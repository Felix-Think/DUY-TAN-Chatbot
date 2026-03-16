from typing import List
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_core.documents import Document
from src.config.settings import settings

class MarkdownLoader:
    def __init__(self, sources_path: str = str(settings.SOURCES_PATH)):
        self.sources_path = sources_path

    def load(self) -> List[Document]:
        """Loads all markdown files from the sources directory."""
        print(f"Loading documents from: {self.sources_path}")
        loader = DirectoryLoader(
            self.sources_path,
            glob="**/*.md",
            loader_cls=UnstructuredMarkdownLoader,
            show_progress=True
        )
        docs = loader.load()
        print(f"Loaded {len(docs)} document(s).")
        return docs

if __name__ == "__main__":
    # Test loader
    loader = MarkdownLoader()
    documents = loader.load()
    if documents:
        print(f"First document preview: {documents[0].page_content[:200]}...")
