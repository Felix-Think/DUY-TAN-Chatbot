import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path
from typing import Iterable


ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.agent.retriever import AdmissionRetriever


DEFAULT_INPUT = ROOT_DIR / "tests" / "test_case_raw.csv"
DEFAULT_OUTPUT = ROOT_DIR / "tests" / "test_case_raw_results.csv"


def normalize_text(text: str) -> str:
    """Normalizes text for stable exact-snippet checks across raw chunks."""
    normalized = unicodedata.normalize("NFC", text or "")
    normalized = normalized.replace("–", "-").replace("—", "-")
    normalized = normalized.casefold()
    return re.sub(r"\s+", " ", normalized).strip()


def split_keywords(value: str) -> list[str]:
    return [item.strip() for item in (value or "").split("|") if item.strip()]


def source_names(docs: Iterable) -> list[str]:
    names = []
    for doc in docs:
        source = str(doc.metadata.get("source", ""))
        names.append(Path(source).name if source else "")
    return names


def find_first_evidence(docs: list, expected_keywords: list[str]) -> tuple[int | None, str]:
    normalized_keywords = [normalize_text(keyword) for keyword in expected_keywords]
    for index, doc in enumerate(docs, start=1):
        normalized_content = normalize_text(doc.page_content)
        if any(keyword in normalized_content for keyword in normalized_keywords):
            return index, normalized_content[:500]
    return None, ""


def keyword_recall(raw_context: str, expected_keywords: list[str]) -> tuple[float, list[str]]:
    if not expected_keywords:
        return 0.0, []

    normalized_context = normalize_text(raw_context)
    missing = [
        keyword
        for keyword in expected_keywords
        if normalize_text(keyword) not in normalized_context
    ]
    score = (len(expected_keywords) - len(missing)) / len(expected_keywords)
    return score, missing


def evaluate(input_path: Path, output_path: Path, k: int, fail_under: float) -> float:
    retriever = AdmissionRetriever(k=k)
    results = []

    with input_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {"id", "test_category", "input", "expected_keywords"}
        missing_columns = required - set(reader.fieldnames or [])
        if missing_columns:
            raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

        for row in reader:
            query = row["input"].strip()
            docs = retriever.get_relevant_documents(query)
            raw_context = "\n\n".join(doc.page_content for doc in docs)
            expected_keywords = split_keywords(row.get("expected_keywords", ""))
            score, missing_keywords = keyword_recall(raw_context, expected_keywords)
            first_evidence_rank, evidence_preview = find_first_evidence(
                docs,
                expected_keywords,
            )
            expected_source = row.get("expected_source", "").strip()
            retrieved_sources = source_names(docs)
            source_hit = (
                not expected_source
                or any(expected_source == source for source in retrieved_sources)
            )

            results.append({
                "ID": row["id"],
                "Test_Category": row["test_category"],
                "Input": query,
                "Expected_Source": expected_source,
                "Retrieved_Sources": " | ".join(retrieved_sources),
                "Source_Hit": source_hit,
                "Hit_Count": len(expected_keywords) - len(missing_keywords),
                "Keyword_Count": len(expected_keywords),
                "Score": round(score, 4),
                "Missing_Keywords": " | ".join(missing_keywords),
                "First_Evidence_Rank": first_evidence_rank or "",
                "Top_Context_Preview": normalize_text(docs[0].page_content)[:500] if docs else "",
                "Evidence_Context_Preview": evidence_preview,
            })

    scores = [float(row["Score"]) for row in results]
    average = sum(scores) / len(scores) if scores else 0.0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "ID",
            "Test_Category",
            "Input",
            "Expected_Source",
            "Retrieved_Sources",
            "Source_Hit",
            "Hit_Count",
            "Keyword_Count",
            "Score",
            "Missing_Keywords",
            "First_Evidence_Rank",
            "Top_Context_Preview",
            "Evidence_Context_Preview",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Evaluated {len(results)} raw retrieval case(s)")
    print(f"Average keyword recall: {average:.4f}")
    print(f"Minimum required average: {fail_under:.4f}")
    print(f"Results saved to: {output_path}")

    if average < fail_under:
        failed = [row for row in results if float(row["Score"]) < 1.0]
        print("\nCases with missing raw snippets:")
        for row in failed:
            print(f"- ID {row['ID']} score={row['Score']}: {row['Missing_Keywords']}")
        raise SystemExit(1)

    return average


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark raw document retrieval without calling the LLM."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--k",
        type=int,
        default=50,
        help="Number of raw chunks to retrieve for evidence recall checks.",
    )
    parser.add_argument("--fail-under", type=float, default=0.98)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    evaluate(args.input, args.output, args.k, args.fail_under)
