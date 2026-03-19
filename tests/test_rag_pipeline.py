import sys
import os
from pathlib import Path

# Thêm thư mục gốc vào `sys.path` để có thể import từ `src`
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.agent.chatbot import AdmissionChatbot

def test_rag():
    print("Khởi tạo Chatbot (đang load VectorStore và kết nối LLM)...")
    try:
        bot = AdmissionChatbot()
        print("✅ Đã khởi tạo Chatbot thành công!\n")
    except Exception as e:
        print(f"❌ Lỗi khởi tạo: {e}")
        return

    # Câu hỏi test (Dựa vào nội dung file Markdown của đại học Duy Tân)
    test_queries = [
        "Ngành Công nghệ Phần mềm học những môn gì?",
        "Cơ hội việc làm của ngành Trí tuệ Nhân tạo là gì?",
        "Tổ hợp xét tuyển ngành Thiết kế Games là gì?"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"{'-'*50}\n🔍 Câu hỏi {i}: {query}")
        print("Đang tìm kiếm thông tin...⏳")
        
        # Test Retriever riêng lẻ để xem có truy xuất đúng tài liệu chưa
        docs = bot.retriever.invoke(query)
        print("\n📄 Các Chunk (Docs) truy xuất được từ VectorStore:")
        if not docs:
            print("  ⚠️ Không tìm thấy tài liệu phù hợp!")
        else:
            for j, doc in enumerate(docs, 1):
                hang_muc = doc.metadata.get("HangMuc", "Không có header")
                print(f"  [{j}] ### {hang_muc} ({len(doc.page_content)} ký tự)")
                print(f"      {doc.page_content[:150]}...\n")

        try:
            # Lấy câu trả lời từ LLM (sẽ lỗi nếu chưa setup API Key)
            result = bot.ask(query)
            print("🤖 Trả lời của LLM:")
            print(f"> {result['answer']}\n")
            
        except Exception as e:
            print(f"❌ Lỗi khi hỏi LLM (Chưa có API Key?): {e}\n")

if __name__ == "__main__":
    test_rag()
