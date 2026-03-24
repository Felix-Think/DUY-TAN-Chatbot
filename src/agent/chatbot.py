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

    async def astream(self, query: str):
        """Streams a query and yields answer tokens and context."""
        async for event in self.rag_chain.astream_events(
            {"input": query}, 
            version="v2"
        ):
            event_type = event["event"]
            
            # 1. Capture Context (from Retriever)
            if event_type == "on_retriever_end":
                yield {"context": event["data"]["output"]["documents"]}
                
            # 2. Capture Answer Tokens (from Chat Model)
            elif event_type == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield {"token": content}

if __name__ == "__main__":
    # Simple CLI Test
    bot = AdmissionChatbot()
    # while True:
    #     q = input("Nhập câu hỏi: ")
    #     if q == "exit": break
    #     res = bot.ask(q)
    #     print(f"Chatbot: {res['answer']}\n")
