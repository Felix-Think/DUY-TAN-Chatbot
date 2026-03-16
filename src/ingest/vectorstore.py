from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from src.config.settings import settings

class VectorStoreManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.persist_directory = str(settings.CHROMA_PATH)
        self.collection_name = settings.CHROMA_COLLECTION_NAME

    def create_vector_store(self, chunks: List[Document]):
        """Creates or updates the vector store with new chunks."""
        print(f"Creating vector store at: {self.persist_directory}")
        
        # Initialize and store vectors
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        print(f"Successfully saved {len(chunks)} chunks to ChromaDB.")
        return vector_db

    def get_vector_store(self):
        """Loads the existing vector store."""
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=self.collection_name
        )

if __name__ == "__main__":
    # Test vector store logic with mock data
    mock_chunks = [Document(page_content="Đây là ví dụ về dữ liệu tuyển sinh.", metadata={"source": "test.md"})]
    manager = VectorStoreManager()
    # manager.create_vector_store(mock_chunks) # Uncomment to run actual embedding
    print("Vector Store Manager initialized.")
