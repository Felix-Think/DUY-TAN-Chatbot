from typing import List
import tiktoken
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader


class DocumentChunker:
    def __init__(self):
        # Split only on ### headers
        self.headers_to_split_on = [
            ("#", "Nganh"),
            ("##", "ChuyenNganh"),
            ("###", "HangMuc"),
        ]

        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on,
            strip_headers=True
        )

    def split(self, documents: List[Document]) -> List[Document]:
        """Splits documents by ### Markdown headers only (no recursive splitting)."""
        all_chunks = []

        for doc in documents:
            header_chunks = self.markdown_splitter.split_text(doc.page_content)

            # Carry over original metadata (e.g. source filename)
            for chunk in header_chunks:
                chunk.metadata.update(doc.metadata)

                # Include headers in the content so the LLM knows the section context
                headers_text = ", ".join(f"{v}" for k, v in chunk.metadata.items() if k != "source")
                if headers_text:
                    chunk.page_content = f"[{headers_text}]\n{chunk.page_content}"

            all_chunks.extend(header_chunks)

        print(f"Created {len(all_chunks)} chunks from {len(documents)} document(s).")
        return all_chunks


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))


if __name__ == "__main__":
    loader = TextLoader("Documents/SCA_Major.md", encoding="utf-8")
    data = loader.load()

    chunker = DocumentChunker()
    chunks = chunker.split(data)

    print("\n=== Token count per chunk ===")
    token_counts = []
    for i, chunk in enumerate(chunks):
        n_tokens = count_tokens(chunk.page_content)
        token_counts.append(n_tokens)
        header = chunk.metadata.get("HangMuc", "(no header)")
        print(f"Chunk {i+1:>3} | {n_tokens:>5} tokens | ### {header}")
        print(f"         metadata: {chunk.metadata}")

    print(f"\nMin : {min(token_counts)}")
    print(f"Max : {max(token_counts)}")
    print(f"Avg : {sum(token_counts) / len(token_counts):.1f}")
    print(f"Total: {sum(token_counts)}")
