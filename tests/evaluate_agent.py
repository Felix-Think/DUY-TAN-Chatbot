import csv
import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
from typing import List
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

    def evaluate(self, playbook_path: str, output_path: str):
        print(f"--- Starting Evaluation using {playbook_path} ---")
        
        results = []
        with open(playbook_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                q_id = row['id']
                input_q = row['input']
                target = row['target']
                
                print(f"Evaluating ID {q_id}: {input_q}")
                
                # 1. Get Agent Output
                res = self.bot.ask(input_q)
                output_a = res['answer']
                
                # 2. Calculate Similarity
                v_target = self.embeddings.embed_query(target)
                v_output = self.embeddings.embed_query(output_a)
                score = self.cosine_similarity(v_target, v_output)
                
                results.append({
                    "ID": q_id,
                    "Input": input_q,
                    "Output": output_a,
                    "Target": target,
                    "Score": round(float(score), 4)
                })

        # 3. Write to CSV
        fieldnames = ["ID", "Input", "Output", "Target", "Score"]
        with open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
            
        print(f"--- Evaluation Completed. Results saved to {output_path} ---")

if __name__ == "__main__":
    # Ensure numpy is available or use a fallback
    evaluator = Evaluator()
    evaluator.evaluate("tests/playbook.csv", "tests/answerbook.csv")
