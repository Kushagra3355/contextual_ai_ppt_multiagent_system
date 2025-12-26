from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_core.documents import Document

LOADERS = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".docx": Docx2txtLoader,
}


def load_documents(directory: str) -> list[Document]:
    documents = []

    for file_path in Path(directory).rglob("*"):
        loader_cls = LOADERS.get(file_path.suffix.lower())
        if not loader_cls:
            continue

        loader = loader_cls(str(file_path))
        docs = loader.load()

        for doc in docs:
            doc.metadata = {
                "source": file_path.name,
                "path": str(file_path),
                "ext": file_path.suffix.lower(),
            }
            documents.append(doc)

    if not documents:
        raise RuntimeError("No supported documents found")

    return documents
