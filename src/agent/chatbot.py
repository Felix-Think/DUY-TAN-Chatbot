from langchain_openai import ChatOpenAI
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from src.agent.retriever import AdmissionRetriever
from src.agent.prompts import get_admission_prompt
from src.config.settings import settings

class AdmissionChatbot:
    def __init__(self):
        # 1. Setup Retriever
        self.retriever = AdmissionRetriever().vector_db.as_retriever(
            search_kwargs={"k": 5}
        )
        
        # 2. Setup LLM
        self.llm = ChatOpenAI(
            model=settings.CHAT_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0
        )
        
        # 3. Setup Prompt
        self.prompt = get_admission_prompt()
        
        # 4. Create RAG Chain
        self.combine_docs_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, self.combine_docs_chain)

    def ask(self, query: str):
        """Processes a query and returns the answer."""
        response = self.rag_chain.invoke({"input": query})
        return {
            "answer": response["answer"],
            "context": response["context"]
        }

if __name__ == "__main__":
    # Simple CLI Test
    bot = AdmissionChatbot()
    # while True:
    #     q = input("Nhập câu hỏi: ")
    #     if q == "exit": break
    #     res = bot.ask(q)
    #     print(f"Chatbot: {res['answer']}\n")
