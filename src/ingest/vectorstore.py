from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
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
    from langchain_core.embeddings import FakeEmbeddings

    print("Testing VectorStoreManager with FakeEmbeddings...")
    
    # 1. Initialize manager but replace real embeddings with fake ones
    manager = VectorStoreManager()
    manager.embeddings = FakeEmbeddings(size=1536) # Same dimension as text-embedding-3-small
    manager.persist_directory = "./chroma_db_mock" # Use a separate test DB
    
    # 2. Create mock data
    mock_chunks = [
        Document(page_content="Đây là ví dụ về dữ liệu tuyển sinh.", metadata={"source": "test.md"}),
        Document(page_content="Ngành Công nghệ Phần mềm học lập trình.", metadata={"source": "test.md"})
    ]
    
    # 3. Test creation
    print("\n--- Testing create_vector_store ---")
    vector_db = manager.create_vector_store(mock_chunks)
    
    # 4. Test retrieval
    print("\n--- Testing get_vector_store ---")
    retrieved_db = manager.get_vector_store()
    
    # 5. Test a quick search
    results = retrieved_db.similarity_search("AI", k=1)
    print("\n--- Search Results ---")
    for res in results:
        print(f"Content: {res.page_content}")
        print(f"Metadata: {res.metadata}")
        
    print("\nVectorStore mock test completed successfully!")
