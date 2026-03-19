from src.ingest.loader import MarkdownLoader
from src.ingest.chunker import DocumentChunker
from src.ingest.vectorstore import VectorStoreManager

def main():
    print("--- Starting Data Ingestion Pipeline ---")
    
    # 1. Load Documents
    loader = MarkdownLoader()
    documents = loader.load()
    
    if not documents:
        print("No documents found in the sources directory. Please check your files.")
        return

    # 2. Chunk Documents
    chunker = DocumentChunker()
    chunks = chunker.split(documents)
    
    # 3. Create Vector Store
    vector_manager = VectorStoreManager()
    vector_manager.create_vector_store(chunks)
    
    print("--- Ingestion Pipeline Completed Successfully ---")

if __name__ == "__main__":
    main()
