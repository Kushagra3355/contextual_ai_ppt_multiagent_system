import streamlit as st
import time
import os
import sys
from pathlib import Path
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import local modules
from orchestrator.ppt_graph import run_ppt_generation
from orchestrator.agent_state import PPTAgentState
from rag_pipeline.pipeline import RAGPipeline
from agents.export_agent import ExportAgent

# Page configuration
st.set_page_config(
    page_title="AI PPT Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .success-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #E8F5E9;
        border-left: 4px solid #4CAF50;
    }
    .info-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown(
    '<div class="main-header">📊 AI PowerPoint Generator</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-header">Transform your documents into professional presentations using AI</div>',
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown(
        """
    1. **Enter Topic**: Main subject for your presentation
    2. **Add Context** (optional): Additional information
    3. **Upload Documents**: PDF, TXT, DOCX files
    4. **Generate**: Click to start AI processing
    5. **Download**: Get your presentation when ready
    """
    )

    st.divider()

    st.header("🔍 About")
    st.markdown(
        """
    This tool uses a multi-agent AI system to:
    - Generate structured outlines
    - Expand content using RAG
    - Review and validate information
    - Export professional PPT files
    """
    )

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 Create Your Presentation")

    # Input form
    with st.form("generate_form", clear_on_submit=False):
        topic = st.text_input(
            "Presentation Topic *",
            placeholder="e.g., Machine Learning in Healthcare",
            help="The main topic for your presentation",
        )

        slides_count = st.slider(
            "Number of Slides",
            min_value=3,
            max_value=20,
            value=7,
            help="Total number of slides to generate",
        )

        context = st.text_area(
            "Additional Context (Optional)",
            placeholder="Add any specific requirements, target audience, or key points to include...",
            height=100,
            help="Provide extra context to guide the AI",
        )

        st.markdown("---")

        uploaded_files = st.file_uploader(
            "📁 Upload Reference Documents",
            accept_multiple_files=True,
            type=["pdf", "txt", "docx", "doc"],
            help="Upload documents that will be used as reference material",
        )

        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
            with st.expander("View uploaded files"):
                for f in uploaded_files:
                    file_size = len(f.getvalue()) / 1024  # KB
                    st.text(f"📄 {f.name} ({file_size:.1f} KB)")

        submit = st.form_submit_button(
            "🚀 Generate Presentation", use_container_width=True
        )

    # Handle form submission
    if submit:
        if not topic:
            st.error("❌ Please enter a topic for your presentation")
        elif not uploaded_files:
            st.error("❌ Please upload at least one reference document")
        else:
            try:
                # Create temporary directory for uploaded files
                temp_dir = tempfile.mkdtemp()
                output_dir = "outputs"

                with st.spinner("📁 Processing uploaded files..."):
                    # Save uploaded files to temp directory
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getvalue())

                    st.info(f"✅ Saved {len(uploaded_files)} files")

                with st.spinner("🔄 Ingesting documents into RAG pipeline..."):
                    # Initialize RAG pipeline and ingest documents
                    rag = RAGPipeline()
                    rag.ingest(temp_dir)
                    rag.load()
                    st.info("✅ Documents processed and indexed")

                with st.spinner("🤖 Generating presentation outline..."):
                    # Run the PPT generation workflow
                    progress_bar = st.progress(0)
                    st.session_state["current_stage"] = "Outline Generation"
                    progress_bar.progress(25)

                    result_dict = run_ppt_generation(
                        topic=topic, slides=slides_count, context=context or ""
                    )

                    # Convert dict result to PPTAgentState object
                    result_state = PPTAgentState(**result_dict)

                    progress_bar.progress(75)
                    st.session_state["current_stage"] = "Exporting presentation"

                with st.spinner("📊 Exporting PowerPoint file..."):
                    # Export to PowerPoint
                    ExportAgent(result_state, output_dir=output_dir)
                    progress_bar.progress(100)
                    st.session_state["current_stage"] = "Complete"

                # Clean up temp directory
                shutil.rmtree(temp_dir, ignore_errors=True)

                # Store result in session state - ExportAgent saves as generated_ppt.pptx
                output_path = os.path.join(output_dir, "generated_ppt.pptx")

                st.session_state["output_file"] = output_path
                st.session_state["topic"] = topic
                st.session_state["generation_complete"] = True

                st.success("✅ Presentation generated successfully!")

            except Exception as e:
                st.error(f"❌ Generation failed: {str(e)}")
                with st.expander("View error details"):
                    st.code(str(e))
                    import traceback

                    st.code(traceback.format_exc())

with col2:
    st.header("💡 Tips")
    st.info(
        """
    **For best results:**
    - Be specific with your topic
    - Upload relevant, quality documents
    - Provide clear context
    - Wait for processing to complete
    """
    )

    st.success(
        """
    **Supported formats:**
    - PDF documents
    - Text files (.txt)
    - Word documents (.docx)
    """
    )

# Results section
st.markdown("---")

if st.session_state.get("generation_complete"):
    output_file = st.session_state.get("output_file")

    st.header("✅ Generation Complete!")

    if output_file and os.path.exists(output_file):
        # Read file for download
        with open(output_file, "rb") as f:
            ppt_bytes = f.read()

        st.download_button(
            label="⬇️ Download Presentation",
            data=ppt_bytes,
            file_name="generated_ppt.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True,
        )
    else:
        st.warning("Output file not found. It may have been moved or deleted.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🤖 Powered by Multi-Agent AI System | Built with Streamlit & LangGraph</p>
    </div>
    """,
    unsafe_allow_html=True,
)
