from typing import Optional

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from src.agent.retriever import AdmissionRetriever
from src.agent.prompts import get_admission_prompt, get_contextualize_prompt
from src.config.settings import settings

class AdmissionChatbot:
    def __init__(self, max_history_messages: int = 8):
        # 1. Setup Retriever
        self.retriever = AdmissionRetriever().vector_db.as_retriever(
            search_kwargs={"k": 5}
        )
        self.max_history_messages = max_history_messages
        self.history_store: dict[str, list[BaseMessage]] = {}
        
        # 2. Setup LLM
        self.llm = ChatOpenAI(
            model=settings.CHAT_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0
        )
        
        # 3. Setup Prompts
        self.prompt = get_admission_prompt()
        self.contextualize_prompt = get_contextualize_prompt()
        
        # 4. Create RAG Components
        self.combine_docs_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.query_rewriter = self.contextualize_prompt | self.llm | StrOutputParser()

    def _get_history(self, session_id: Optional[str]) -> list[BaseMessage]:
        if not session_id:
            return []
        return list(self.history_store.get(session_id, []))

    def _save_exchange(self, session_id: Optional[str], query: str, answer: str) -> None:
        if not session_id:
            return

        history = self.history_store.setdefault(session_id, [])
        history.extend([HumanMessage(content=query), AIMessage(content=answer)])
        self.history_store[session_id] = history[-self.max_history_messages:]

    def clear_history(self, session_id: str) -> None:
        """Clears memory for one chat session."""
        self.history_store.pop(session_id, None)

    def contextualize_query(self, query: str, session_id: Optional[str] = None) -> str:
        """Rewrites a follow-up query into a standalone retrieval query."""
        history = self._get_history(session_id)
        if not history:
            return query

        rewritten_query = self.query_rewriter.invoke({
            "input": query,
            "chat_history": history,
        }).strip()
        return rewritten_query or query

    def ask(self, query: str, session_id: Optional[str] = None):
        """Processes a query and returns the answer."""
        chat_history = self._get_history(session_id)
        retrieval_query = self.contextualize_query(query, session_id)
        context = self.retriever.invoke(retrieval_query)
        answer = self.combine_docs_chain.invoke({
            "input": query,
            "chat_history": chat_history,
            "context": context,
        })
        self._save_exchange(session_id, query, answer)
        return {
            "answer": answer,
            "context": context,
            "retrieval_query": retrieval_query,
        }

    async def astream(self, query: str, session_id: Optional[str] = None):
        """Streams a query and yields answer tokens and context."""
        chat_history = self._get_history(session_id)
        retrieval_query = query
        if chat_history:
            retrieval_query = (await self.query_rewriter.ainvoke({
                "input": query,
                "chat_history": chat_history,
            })).strip() or query

        context = await self.retriever.ainvoke(retrieval_query)
        if context:
            yield {"context": context, "retrieval_query": retrieval_query}

        answer_parts = []
        async for chunk in self.combine_docs_chain.astream({
            "input": query,
            "chat_history": chat_history,
            "context": context,
        }):
            token = chunk if isinstance(chunk, str) else getattr(chunk, "content", "")
            if token:
                answer_parts.append(token)
                yield {"token": token}

        self._save_exchange(session_id, query, "".join(answer_parts))

if __name__ == "__main__":
    import asyncio
    # Simple CLI Test
    async def main():
        bot = AdmissionChatbot()
        async for chunk in bot.astream("Chào bạn", session_id="cli"):
            print(chunk)
    
    asyncio.run(main())
