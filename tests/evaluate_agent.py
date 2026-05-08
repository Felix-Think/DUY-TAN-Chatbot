import csv
import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
from langchain_openai import OpenAIEmbeddings
from src.agent.chatbot import AdmissionChatbot
from src.config.settings import settings


class Evaluator:
    def __init__(self):
        self.bot = AdmissionChatbot()
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )

    def cosine_similarity(self, v1, v2):
        """Calculates cosine similarity between two vectors."""
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        return dot_product / (norm_v1 * norm_v2)

    def evaluate(self, input_path: str, output_path: str):
        """
        Reads test cases from input CSV, queries the agent for each,
        computes cosine similarity, and writes results to output CSV.

        Input CSV columns  : id, test_category, input, target, expected_behavior,
                             out_of_scope, priority, notes
        Output CSV columns : ID, Test_Category, Input, Target, Output, Score
        """
        print(f"--- Starting Evaluation: {input_path} ---")

        results = []
        with open(input_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                q_id = row["id"]
                test_category = row["test_category"]
                input_q = row["input"]
                target = row["target"]

                print(f"  [{q_id}/{test_category}] {input_q}")

                # 1. Get agent output
                try:
                    res = self.bot.ask(input_q)
                    output_a = res["answer"]
                except Exception as e:
                    output_a = f"ERROR: {e}"
                    print(f"    ! Agent error: {e}")

                # 2. Calculate cosine similarity
                try:
                    v_target = self.embeddings.embed_query(target)
                    v_output = self.embeddings.embed_query(output_a)
                    score = self.cosine_similarity(v_target, v_output)
                except Exception as e:
                    score = -1.0
                    print(f"    ! Embedding error: {e}")

                results.append({
                    "ID": q_id,
                    "Test_Category": test_category,
                    "Input": input_q,
                    "Target": target,
                    "Output": output_a,
                    "Score": round(float(score), 4)
                })

        # 3. Write output CSV
        fieldnames = ["ID", "Test_Category", "Input", "Target", "Output", "Score"]
        with open(output_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        # 4. Summary statistics
        valid_scores = [r["Score"] for r in results if r["Score"] >= 0]
        if valid_scores:
            avg = np.mean(valid_scores)
            std = np.std(valid_scores)
            mx  = max(valid_scores)
            mn  = min(valid_scores)
            print(f"\n=== Summary (n={len(valid_scores)}) ===")
            print(f"  Average : {avg:.4f}")
            print(f"  Std Dev : {std:.4f}")
            print(f"  Max     : {mx:.4f}")
            print(f"  Min     : {mn:.4f}")

            # Breakdown by threshold
            good = sum(1 for s in valid_scores if s >= 0.75)
            avg_ = sum(1 for s in valid_scores if 0.65 <= s < 0.75)
            low  = sum(1 for s in valid_scores if s < 0.65)
            print(f"  TỐT (≥0.75)     : {good}")
            print(f"  TRUNG BÌNH      : {avg_}")
            print(f"  THẤP (<0.65)    : {low}")

        print(f"\n--- Results saved to {output_path} ---")


if __name__ == "__main__":
    evaluator = Evaluator()
    evaluator.evaluate("tests/testcase.csv", "tests/testcase_answer.csv")
