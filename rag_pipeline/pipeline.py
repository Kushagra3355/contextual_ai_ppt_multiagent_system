from rag_pipeline.loader import load_documents
from rag_pipeline.splitter import split_documents
from rag_pipeline.vector_store import build_vectorstore, load_vectorstore
from rag_pipeline.retriever import get_retriever


class RAGPipeline:
    def __init__(self):
        self.retriever = None

    def ingest(self, data_dir: str):
        """
        Run ingestion: load → split → embed → store
        """
        documents = load_documents(data_dir)
        chunks = split_documents(documents, 800, 120)
        build_vectorstore(chunks)

        print(f"✅ Ingested {len(chunks)} chunks")

    def load(self):
        """
        Load existing vectorstore and create retriever
        """
        vectorstore = load_vectorstore()
        if not vectorstore:
            raise RuntimeError("Vector DB not found. Run ingest() first.")

        self.retriever = get_retriever(vectorstore)

    def query(self, question: str):
        """
        Retrieve relevant documents for a query
        """
        if not self.retriever:
            raise RuntimeError("Pipeline not loaded. Call load() first.")

        vectorstore = load_vectorstore()
        return vectorstore.similarity_search(question, k=5)
