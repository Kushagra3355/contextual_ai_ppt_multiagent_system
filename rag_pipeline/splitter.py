import re
import os
from copy import deepcopy
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:
    """Clean and normalize text to reduce redundancy."""

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s\.\,\;\:\!\?\-\(\)\[\]\/]", "", text)
    return text.strip()


def split_documents(documents, chunk_size, chunk_overlap):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", ";", " ", ""],
    )
    cleaned_docs = []
    for doc in documents:
        new_doc = deepcopy(doc)
        new_doc.page_content = clean_text(doc.page_content)

        source = new_doc.metadata.get("source", "unknown")
        new_doc.metadata["filename"] = os.path.basename(source)

        cleaned_docs.append(new_doc)

    chunks = splitter.split_documents(cleaned_docs)
    
    for idx, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = idx

    # print(f"Total chunks created: {len(chunks)}")
    return chunks
