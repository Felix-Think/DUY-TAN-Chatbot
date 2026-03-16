from typing import List
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class DocumentChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        # 1. Define headers to split on
        self.headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        
        # 2. Markdown Header Splitter
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on
        )
        
        # 3. Secondary splitter for large sections
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def split(self, documents: List[Document]) -> List[Document]:
        """Splits documents using Markdown headers and recursive splitting."""
        all_chunks = []
        
        for doc in documents:
            # First split by markdown headers
            header_chunks = self.markdown_splitter.split_text(doc.page_content)
            
            # Further split each header chunk into smaller pieces if needed
            chunks = self.text_splitter.split_documents(header_chunks)
            
            # Carry over original metadata if any (like source filename)
            for chunk in chunks:
                chunk.metadata.update(doc.metadata)
            
            all_chunks.extend(chunks)
        
        print(f"Created {len(all_chunks)} chunks from {len(documents)} document(s).")
        return all_chunks

if __name__ == "__main__":
    # Mock test
    mock_doc = Document(
        page_content="# Trường KHMT\n## Ngành TTNT\nMô tả chi tiết ngành TTNT...",
        metadata={"source": "test.md"}
    )
    chunker = DocumentChunker()
    test_chunks = chunker.split([mock_doc])
    for i, c in enumerate(test_chunks):
        print(f"Chunk {i} Metadata: {c.metadata}")
        print(f"Chunk {i} Content: {c.page_content[:100]}\n")
        
