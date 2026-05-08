import sys
import uuid
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.agent.chatbot import AdmissionChatbot


QUESTION_1 = "ngành khoa học máy tính có những ngành nào?"
QUESTION_2 = "Nó có học phí bao nhiêu"


def normalize(text: str) -> str:
    return " ".join((text or "").casefold().split())


def source_names(docs) -> str:
    names = []
    for doc in docs:
        source = str(doc.metadata.get("source", ""))
        names.append(Path(source).name if source else "")
    return " | ".join(names)


def preview(text: str, limit: int = 700) -> str:
    compact = " ".join((text or "").split())
    return compact[:limit]


def main() -> None:
    session_id = f"memory-backtest-{uuid.uuid4()}"
    bot = AdmissionChatbot()

    baseline_docs = bot.retriever.invoke(QUESTION_2)

    turn_1 = bot.ask(QUESTION_1, session_id=session_id)
    turn_2 = bot.ask(QUESTION_2, session_id=session_id)

    rewritten_query = turn_2["retrieval_query"]
    normalized_query = normalize(rewritten_query)
    rewrite_passed = (
        "khoa học máy tính" in normalized_query
        and "học phí" in normalized_query
        and "nó" not in normalized_query
    )

    print("=== Memory Back-test: follow-up question resolution ===")
    print(f"Session ID: {session_id}")
    print(f"Turn 1 user query: {QUESTION_1}")
    print(f"Turn 2 user query: {QUESTION_2}")
    print()
    print(f"Baseline retrieval query: {QUESTION_2}")
    print(f"Baseline sources: {source_names(baseline_docs)}")
    print()
    print(f"Memory-aware retrieval query: {rewritten_query}")
    print(f"Memory-aware sources: {source_names(turn_2['context'])}")
    print()
    print("Turn 1 answer preview:")
    print(preview(turn_1["answer"]))
    print()
    print("Turn 2 answer preview:")
    print(preview(turn_2["answer"]))
    print()
    print("Expected rewrite: replace 'Nó' with 'ngành Khoa học Máy tính'.")
    print(f"Rewrite check: {'PASS' if rewrite_passed else 'FAIL'}")
    print()
    print(
        "Note: data/sources currently has no explicit tuition/học phí entry, "
        "so a correct final answer may say the tuition information is unavailable "
        "after retrieving with the corrected subject."
    )

    if not rewrite_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
