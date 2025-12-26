from langchain_text_splitters import RecursiveCharacterTextSplitter
import hashlib

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", ";", " ", ""],
    )

    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        chunk.metadata["chunk_id"] = hashlib.sha1(
            (chunk.page_content + chunk.metadata["source"]).encode()
        ).hexdigest()

    return chunks
