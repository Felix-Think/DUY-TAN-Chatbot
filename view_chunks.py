import os
import sys

# Add project root to sys.path so we can import 'src' when running directly
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.ingest.vectorstore import VectorStoreManager

def main():
    print("Loading Vector Store...")
    manager = VectorStoreManager()
    db = manager.get_vector_store()
    
    # Access the underlying chroma collection
    collection = db._collection
    
    # Get all documents
    print("Fetching chunks...")
    result = collection.get()
    
    ids = result.get('ids', [])
    documents = result.get('documents', [])
    metadatas = result.get('metadatas', [])
    
    total_chunks = len(ids)
    print(f"\nTotal chunks in the vector store: {total_chunks}\n")
    
    if total_chunks == 0:
        print("The vector store is currently empty.")
        return
        
    print("-" * 50)
    # Print the first 10 chunks as an example
    limit = total_chunks
    print(f"Displaying the first {limit} chunks:\n")
    
    for i in range(limit):
        print(f"Chunk {i+1} (ID: {ids[i]}):")
        print(f"Metadata: {metadatas[i]}")
        
        # Truncate content for readability
        content = documents[i]
        display_content = content if len(content) <= 300 else content[:300] + "..."
        print(f"Content:\n{display_content}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()
