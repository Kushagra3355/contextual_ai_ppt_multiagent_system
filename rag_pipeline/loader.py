from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
import os


def load_documents(file_path):

    documents = []
    if isinstance(file_path, str):
        # Handle directory path
        file_paths = []
        for root, _, files in os.walk(file_path):
            for file in files:
                file_paths.append(os.path.join(root, file))
        file_path = file_paths

    for path in file_path:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(path)
        elif ext == ".txt":
            loader = TextLoader(path)
        elif ext == ".docx":
            loader = Docx2txtLoader(path)
        else:
            print(f"Skipping unsuported files: {path}")
            continue
        documents.extend(loader.load())

    return documents
