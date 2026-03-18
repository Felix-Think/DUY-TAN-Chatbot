import os
import sys

# Add project root to sys.path so we can import 'src' when running directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from typing import List
from langchain_core.documents import Document
from src.ingest.vectorstore import VectorStoreManager
class AdmissionRetriever:
    def __init__(self, k: int = 5):
        self.vector_manager = VectorStoreManager()
        self.vector_db = self.vector_manager.get_vector_store()
        self.k = k

    def get_relevant_documents(self, query: str) -> List[Document]:
        """Retrieves top K relevant documents for a given query."""
        print(f"Retrieving context for query: {query}")
        docs = self.vector_db.similarity_search(query, k=self.k)
        return docs

if __name__ == "__main__":
    # Test retriever
    retriever = AdmissionRetriever()
    docs = retriever.get_relevant_documents("Tổ hợp xét tuyển ngành của Thiết kế Games là gì?")
    for d in docs: 
        print(d.metadata)
