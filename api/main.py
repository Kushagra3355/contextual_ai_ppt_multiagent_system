from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import shutil
import uuid
from datetime import datetime

try:
    from rag_pipeline.pipeline import RAGPipeline
    from orchestrator.ppt_graph import run_ppt_generation, get_workflow_status
    from orchestrator.agent_state import ContentSlidesResponse
except ImportError as e:
    print(f"Warning: Could not import some modules: {e}")
    RAGPipeline = None

app = FastAPI(title="PPT Generator API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage for task status
task_storage: Dict[str, Dict[str, Any]] = {}

# Initialize RAG pipeline with error handling
try:
    rag_pipeline = RAGPipeline() if RAGPipeline else None
except Exception as e:
    print(f"Warning: Could not initialize RAG pipeline: {e}")
    rag_pipeline = None


# Pydantic models
class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str


class PPTResponse(BaseModel):
    task_id: str
    status: str
    output_file: Optional[str] = None
    filename: Optional[str] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    return {
        "message": "PPT Generator API - Upload documents and generate presentations",
        "version": "1.0.0",
    }


@app.post("/generate-ppt", response_model=PPTResponse)
async def generate_presentation(
    background_tasks: BackgroundTasks,
    topic: str = Form(...),
    context: str = Form(""),
    files: List[UploadFile] = File(...),
):
    """Upload documents and generate PowerPoint presentation in one step"""
    task_id = str(uuid.uuid4())

    try:
        # Create upload directory
        upload_dir = f"data/uploads/{task_id}"
        os.makedirs(upload_dir, exist_ok=True)

        # Save uploaded files
        file_paths = []
        for file in files:
            file_path = os.path.join(upload_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_paths.append(file_path)

        # Initialize task status
        task_storage[task_id] = {
            "status": "processing",
            "message": "Processing documents and generating presentation...",
            "created_at": datetime.now(),
            "topic": topic,
            "context": context,
            "files": file_paths,
        }

        # Run complete workflow in background
        background_tasks.add_task(
            generate_complete_ppt_task, task_id, upload_dir, topic, context
        )

        return PPTResponse(task_id=task_id, status="processing")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """Get status of a background task"""
    if task_id not in task_storage:
        raise HTTPException(status_code=404, detail="Task not found")

    task = task_storage[task_id]

    # Enhanced status for PPT generation
    if "workflow_state" in task:
        workflow_status = get_workflow_status(task["workflow_state"])
        task["detailed_status"] = workflow_status

    return task


@app.get("/download/{task_id}")
async def download_presentation(task_id: str):
    """Download generated PowerPoint file"""
    if task_id not in task_storage:
        raise HTTPException(status_code=404, detail="Task not found")

    task = task_storage[task_id]

    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task not completed")

    if "output_file" not in task or not os.path.exists(task["output_file"]):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=task["output_file"],
        filename=task.get("filename", "presentation.pptx"),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if RAG pipeline is available
        rag_status = "not_available"
        if rag_pipeline:
            try:
                rag_pipeline.load()
                rag_status = "available"
            except:
                rag_status = "not_ready"

        return {
            "status": "healthy",
            "timestamp": datetime.now(),
            "rag_pipeline": rag_status,
            "active_tasks": len(
                [t for t in task_storage.values() if t["status"] == "processing"]
            ),
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


# Background task functions
async def generate_complete_ppt_task(
    task_id: str, data_path: str, topic: str, context: str
):
    """Complete workflow: ingest documents and generate PPT"""
    try:
        if not rag_pipeline:
            raise RuntimeError("RAG pipeline not available")

        # Step 1: Ingest documents
        task_storage[task_id]["status"] = "processing"
        task_storage[task_id]["message"] = "Processing documents..."

        # Ensure directories exist
        os.makedirs("vector_db", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        rag_pipeline.ingest(data_path)

        # Step 2: Generate PPT
        task_storage[task_id]["message"] = "Generating presentation with AI agents..."

        # Run the complete workflow
        result = run_ppt_generation(topic, context)

        # Store workflow state for status tracking
        task_storage[task_id]["workflow_state"] = result

        if result.get("export_status") == "success":
            task_storage[task_id]["status"] = "completed"
            task_storage[task_id]["message"] = "Presentation generated successfully"
            task_storage[task_id]["output_file"] = result.get("output_file")
            task_storage[task_id]["filename"] = result.get("filename")
            task_storage[task_id]["completed_at"] = datetime.now()
        else:
            task_storage[task_id]["status"] = "failed"
            task_storage[task_id]["message"] = "PPT generation failed"
            task_storage[task_id]["error"] = result.get("error", "Unknown error")

    except Exception as e:
        task_storage[task_id]["status"] = "failed"
        task_storage[task_id]["message"] = f"Process failed: {str(e)}"
        task_storage[task_id]["error"] = str(e)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
