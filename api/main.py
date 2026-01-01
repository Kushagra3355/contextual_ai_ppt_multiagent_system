from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import sys
import shutil
from pathlib import Path
import uuid
import tempfile

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from orchestrator.ppt_graph import run_ppt_generation
from orchestrator.agent_state import PPTAgentState
from rag_pipeline.pipeline import RAGPipeline
from agents.export_agent import ExportAgent

app = FastAPI(
    title="AI PowerPoint Generator API",
    description="Multi-agent system for generating presentations from documents",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage for sessions
sessions = {}


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI PowerPoint Generator API",
        "version": "1.0.0",
        "status": "running",
    }


@app.post("/generate")
async def generate_presentation(
    topic: str = Form(...),
    slides: int = Form(7),
    context: Optional[str] = Form(""),
    files: Optional[List[UploadFile]] = File(None),
):
    """
    Generate PowerPoint presentation with optional document upload
    """
    try:
        session_id = str(uuid.uuid4())
        temp_dir = None

        # Handle file uploads if provided
        if files:
            temp_dir = tempfile.mkdtemp()

            # Save uploaded files
            for file in files:
                file_ext = Path(file.filename).suffix.lower()
                if file_ext not in [".pdf", ".txt", ".docx", ".doc"]:
                    raise HTTPException(
                        status_code=400, detail=f"Unsupported file type: {file_ext}"
                    )

                file_path = os.path.join(temp_dir, file.filename)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

            # Initialize RAG pipeline
            rag = RAGPipeline()
            rag.ingest(temp_dir)
            rag.load()

        # Run PPT generation
        result_dict = run_ppt_generation(
            topic=topic, slides=slides, context=context or ""
        )

        # Convert to PPTAgentState
        result_state = PPTAgentState(**result_dict)

        # Export to PowerPoint
        output_dir = "outputs"
        ExportAgent(result_state, output_dir=output_dir)

        # Clean up temp directory
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)

        # Store session info
        sessions[session_id] = {
            "status": "completed",
            "topic": topic,
            "ppt_path": os.path.join(output_dir, "generated_ppt.pptx"),
        }

        return {
            "session_id": session_id,
            "message": "Presentation generated successfully",
            "status": "completed",
            "download_url": f"/download/{session_id}",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{session_id}")
async def download_presentation(session_id: str):
    """Download the generated PowerPoint presentation"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    ppt_path = session.get("ppt_path", "outputs/generated_ppt.pptx")

    if not os.path.exists(ppt_path):
        raise HTTPException(status_code=404, detail="Presentation file not found")

    return FileResponse(
        path=ppt_path,
        filename="generated_ppt.pptx",
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )


@app.get("/download")
async def download_latest():
    """Download the latest generated presentation"""
    ppt_path = "outputs/generated_ppt.pptx"

    if not os.path.exists(ppt_path):
        raise HTTPException(status_code=404, detail="Presentation file not found")

    return FileResponse(
        path=ppt_path,
        filename="generated_ppt.pptx",
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )


@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete session data"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    del sessions[session_id]
    return {"message": "Session deleted successfully", "session_id": session_id}


@app.get("/sessions")
async def list_sessions():
    """List all active sessions"""
    return {
        "total_sessions": len(sessions),
        "sessions": [
            {
                "session_id": sid,
                "status": data.get("status"),
                "topic": data.get("topic", "N/A"),
            }
            for sid, data in sessions.items()
        ],
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI PPT Generator"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
