import streamlit as st
import requests
import time


st.set_page_config(page_title="PPT Generator", layout="wide")

st.title("PPT Generator — Streamlit Frontend")

api_base = st.text_input("API base URL", value="http://localhost:8000")

with st.form("generate_form"):
    topic = st.text_input("Topic", help="Main topic for the generated presentation")
    context = st.text_area("Context (optional)")
    uploaded_files = st.file_uploader(
        "Upload documents (PDF, TXT, DOCX, etc.)",
        accept_multiple_files=True,
    )

    submit = st.form_submit_button("Generate PPT")

if submit:
    if not topic:
        st.error("Please enter a topic")
    elif not uploaded_files:
        st.error("Please upload at least one file")
    else:
        try:
            files = []
            for f in uploaded_files:
                content = f.getvalue()
                files.append(
                    ("files", (f.name, content, f.type or "application/octet-stream"))
                )

            data = {"topic": topic, "context": context}
            with st.spinner("Uploading files and starting generation..."):
                resp = requests.post(
                    f"{api_base}/generate-ppt", data=data, files=files, timeout=120
                )

            if resp.status_code == 200:
                result = resp.json()
                task_id = result.get("task_id")
                st.success(f"Generation started — Task ID: {task_id}")
                st.session_state["task_id"] = task_id
            else:
                st.error(f"API error: {resp.status_code} — {resp.text}")

        except Exception as e:
            st.error(f"Request failed: {e}")


def get_task_status(task_id: str):
    try:
        r = requests.get(f"{api_base}/task-status/{task_id}")
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def download_presentation(task_id: str):
    try:
        r = requests.get(f"{api_base}/download/{task_id}", stream=True)
        if r.status_code == 200:
            # try to obtain filename from JSON status
            meta = get_task_status(task_id)
            filename = meta.get("filename") or f"presentation_{task_id}.pptx"
            return r.content, filename
        else:
            st.error(f"Download failed: {r.status_code} - {r.text}")
            return None, None
    except Exception as e:
        st.error(f"Download error: {e}")
        return None, None


if "task_id" in st.session_state:
    task_id = st.session_state["task_id"]
    st.markdown(f"**Active Task ID:** {task_id}")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Check Status"):
            status = get_task_status(task_id)
            st.json(status)

        auto = st.checkbox("Auto-poll until complete", value=False)
        if auto:
            with st.spinner("Polling task status..."):
                for _ in range(60):
                    status = get_task_status(task_id)
                    st.write(status.get("status"))
                    if status.get("status") in ("completed", "failed"):
                        st.json(status)
                        break
                    time.sleep(2)

    with col2:
        status = get_task_status(task_id)
        st.write("Current status:", status.get("status"))
        if status.get("status") == "completed":
            st.success("Task completed — presentation available")
            bytes_data, filename = download_presentation(task_id)
            if bytes_data:
                st.download_button(
                    "Download PPT",
                    data=bytes_data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
        elif status.get("status") == "failed":
            st.error(status.get("message") or status.get("error") or "Task failed")
