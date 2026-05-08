# KHUNG SƯỜN BÁO CÁO HỌC THUẬT

**Đề tài:** Xây dựng Chatbot AI Tư vấn Tuyển sinh dựa trên Retrieval-Augmented Generation (RAG)

**Tech Stack thực tế:** LangChain + ChromaDB + OpenAI GPT-4o-mini + text-embedding-3-small

---

## CẤU TRÚC TỔNG THỂ

```
PHẦN 1: BỐI CẢNH & ĐỊNH NGHĨA
PHẦN 2: KIẾN TRÚC & CÔNG NGHỆ & HỆ THỐNG
   └── 2.5 ĐẠO ĐỨC NGHIÊN CỨU & TRÁCH NHIỆM AI
PHẦN 3: THỰC NGHIỆM & KẾT QUẢ
PHỤ LỤC
TÀI LIỆU THAM KHẢO
```

---

PHỤ LỤC
PHẦN 1: BỐI CẢNH & ĐỊNH NGHĨA
1.1. Giới thiệu tổng quan
- 1.1.1. Bối cảnh nghiên cứu
  - Thực trạng công tác tư vấn tuyển sinh tại Việt Nam
  - Xu hướng ứng dụng AI trong giáo dục
  - Bối cảnh Duy Tan University và nhu cầu số hóa tư vấn tuyển sinh
- 1.1.2. Vấn đề đặt ra
  - Hạn chế của hệ thống tư vấn truyền thống (thời gian, nhân lực, phạm vi)
  - Thách thức trong việc cung cấp thông tin nhanh chóng và chính xác
  - Khó khăn khi xử lý số lượng lớn câu hỏi lặp đi lặp lại
- 1.1.3. Tính cấp thiết của nghiên cứu
  - Nhu cầu tư vấn tuyển sinh ngày càng tăng
  - Tiềm năng ứng dụng RAG trong lĩnh vực giáo dục
  - Giá trị thực tiễn của việc tự động hóa tư vấn

1.2. Cơ sở lý luận
- 1.2.1. Khái niệm Chatbot & AI trong giáo dục
  - Định nghĩa chatbot
  - Phân loại chatbot (rule-based, AI-based, hybrid)
  - Ứng dụng AI chatbot trong giáo dục đại học
- 1.2.2. Retrieval-Augmented Generation (RAG)
  - 1.2.2.1. Khái niệm và nguyên lý hoạt động
    - Lịch sử phát triển RAG
    - Sơ đồ luồng RAG (Query → Retrieval → Augmentation → Generation)
  - 1.2.2.2. Ưu điểm so với LLM thuần túy
    - Giảm thiểu hallucination
    - Cập nhật kiến thức dễ dàng (thay đổi tài liệu nguồn)
    - Chi phí vận hành thấp hơn fine-tuning
    - Đảm bảo nguồn gốc thông tin (traceability)
  - 1.2.2.3. Các kiến trúc RAG phổ biến
    - Naive RAG
    - Advanced RAG (query rewriting, reranking)
    - Modular RAG
- 1.2.3. Vector Database & Semantic Search
  - 1.2.3.1. Khái niệm vector embedding
    - Text embedding và ý nghĩa trong xử lý ngôn ngữ tự nhiên
    - Các mô hình embedding phổ biến (OpenAI, Sentence-BERT, etc.)
  - 1.2.3.2. Semantic Search
    - Khác biệt với keyword search
    - Similarity measures (cosine, euclidean)
  - 1.2.3.3. Vector Database
    - ChromaDB: đặc điểm và ứng dụng
    - So sánh với FAISS, Pinecone, Weaviate
- 1.2.4. Large Language Model (LLM) trong hệ thống RAG
  - 1.2.4.1. Vai trò của LLM trong sinh ngôn ngữ tự nhiên
  - 1.2.4.2. Các LLM phổ biến cho tiếng Việt (GPT-4o, GPT-4o-mini, Claude, etc.)
  - 1.2.4.3. Prompt Engineering trong RAG
    - System prompt, user prompt, context injection
    - Zero-shot, few-shot prompting

1.3. Tổng quan tài liệu & Nghiên cứu liên quan (Literature Review)
- 1.3.1. Ứng dụng AI chatbot trong giáo dục
  - Tình hình nghiên cứu trên thế giới
  - Các nghiên cứu tại Việt Nam
  - Bài học kinh nghiệm từ các dự án tương tự
- 1.3.2. Các hệ thống RAG trong thực tiễn
  - RAG trong hỗ trợ khách hàng
  - RAG trong y tế và pháp lý
  - RAG trong giáo dục
- 1.3.3. Khoảng trống nghiên cứu (Research Gap)
  - Thiếu hệ thống RAG cho tư vấn tuyển sinh tiếng Việt
  - Chưa có nhiều nghiên cứu về chatbot tư vấn tuyển sinh đa ngành
  - Cơ hội nghiên cứu và đóng góp của đề tài

1.4. Mục tiêu & Phạm vi nghiên cứu
- 1.4.1. Mục tiêu tổng quát
  - Xây dựng chatbot AI tư vấn tuyển sinh cho Duy Tan University
  - Sử dụng kiến trúc RAG để đảm bảo câu trả lời chính xác từ tài liệu nguồn
- 1.4.2. Mục tiêu cụ thể
  - Xây dựng pipeline xử lý tài liệu (load → chunk → embed → store)
  - Thiết kế và triển khai hệ thống retrieval hiệu quả
  - Xây dựng prompt phù hợp với vai trò tư vấn tuyển sinh
  - Đánh giá chất lượng câu trả lời của hệ thống
- 1.4.3. Phạm vi và giới hạn
  - Phạm vi: Tư vấn tuyển sinh ngành Khoa học Máy tính & Trí tuệ Nhân tạo, trường Duy Tan University
  - Giới hạn ngôn ngữ: Tiếng Việt
  - Giới hạn dữ liệu: Các tài liệu trong thư mục `data/sources/`
  - Giới hạn công nghệ: Sử dụng OpenAI API






PHẦN 2: KIẾN TRÚC & CÔNG NGHỆ & HỆ THỐNG
2.1. Thiết kế tổng thể hệ thống
- 2.1.1. Sơ đồ kiến trúc hệ thống (System Architecture)
  - Sơ đồ các tầng (layers): Data → Vector Store → Retrieval → Generation
  - Mối liên hệ giữa các thành phần
  - Minh họa bằng sơ đồ kiến trúc
- 2.1.2. Luồng hoạt động tổng quát (End-to-end flow)
  - Luồng xử lý câu hỏi người dùng
  - Luồng đẩy dữ liệu vào hệ thống (ingestion)
- 2.1.3. Các thành phần chính và mối liên hệ
  - MarkdownLoader: Tải tài liệu markdown
  - DocumentChunker: Phân đoạn tài liệu
  - VectorStoreManager: Quản lý ChromaDB
  - AdmissionRetriever: Truy xuất tài liệu liên quan
  - AdmissionChatbot: Điều phối RAG chain

2.2. Tầng Dữ liệu (Data Layer)
- 2.2.1. Nguồn dữ liệu đầu vào
  - 2.2.1.1. Định dạng và cấu trúc tài liệu nguồn
    - Định dạng: Markdown (.md)
    - Nguồn: Thư mục `data/sources/`
    - Loại nội dung: Thông tin ngành, chương trình đào tạo, quy chế tuyển sinh
  - 2.2.1.2. Quy trình thu thập & chuẩn bị dữ liệu
    - Sàng lọc và làm sạch nội dung
    - Chuẩn hóa định dạng markdown
- 2.2.2. Quy trình xử lý tài liệu (Document Processing Pipeline)
  - 2.2.2.1. Tải tài liệu (Document Loading)
    - Sử dụng LangChain DirectoryLoader
    - Xử lý đa tài liệu (batch loading)
  - 2.2.2.2. Phân đoạn tài liệu (Text Chunking)
    - Chiến lược Stage 1: Chia theo tiêu đề markdown (#, ##, ###)
    - Chiến lược Stage 2: Recursive character splitting
    - Tham số: chunk_size=1000, chunk_overlap=100
    - Ưu điểm: Bảo toàn cấu trúc tài liệu
  - 2.2.2.3. Quản lý metadata
    - Gắn metadata cho mỗi chunk (tên file, tiêu đề, đường dẫn)

2.3. Tầng Vector Store (Vector Storage Layer)
- 2.3.1. Lựa chọn vector database
  - So sánh ChromaDB vs FAISS vs Pinecone
  - Lý do chọn ChromaDB (embedded, easy-to-use, LangChain native)
- 2.3.2. Mô hình embedding
  - 2.3.2.1. Lựa chọn: OpenAI `text-embedding-3-small`
    - Lý do: Chi phí thấp, hiệu quả cao, hỗ trợ tiếng Việt
    - Kích thước vector: 1536 dimensions
  - 2.3.2.2. Cấu hình embedding trong hệ thống
- 2.3.3. Cấu hình collection và index
  - Collection name: `admission_data`
  - Đường dẫn lưu trữ: `data/chromadb/`
  - Persistence: Lưu trữ lâu dài, tái sử dụng giữa các lần chạy

2.4. Tầng Tìm kiếm (Retrieval Layer)
- 2.4.1. Chiến lược truy xuất (Retrieval Strategy)
  - 2.4.1.1. Semantic Similarity Search
    - Tính toán độ tương đồng cosine giữa query và documents
  - 2.4.1.2. Tinh chỉnh tham số k
    - Giá trị k=5 (top-5 documents được trả về)
    - Ảnh hưởng của k đến chất lượng câu trả lời
- 2.4.2. Tối ưu hóa truy xuất
  - 2.4.2.1. Đánh giá độ chính xác retrieval
  - 2.4.2.2. Cân bằng giữa precision và recall

2.5. Tầng Sinh ngôn ngữ (Generation Layer)
- 2.5.1. Lựa chọn LLM
  - So sánh GPT-4o vs GPT-4o-mini và những model khác để đánh giá mức độ sử dụng cho phù hợp, tối ưu chi phí và không lãng phí sức mạnh.  
  - Lý do chọn GPT-4o-mini (chi phí thấp, hiệu suất tốt, hỗ trợ tiếng Việt)
- 2.5.2. Xây dựng Prompt Engineering
  - 2.5.2.1. System Prompt
    - Vai trò: Tư vấn tuyển sinh Duy Tan University
    - Ràng buộc: Chỉ sử dụng context được cung cấp
    - Hành vi: Từ chối câu hỏi ngoài phạm vi
    - Ngôn ngữ: Tiếng Việt
  - 2.5.2.2. User Prompt Template
    - Cấu trúc: Câu hỏi + Context + Câu hỏi kèm theo
  - 2.5.2.3. Context Integration
    - Đưa top-k documents vào prompt dưới dạng context
- 2.5.3. RAG Chain orchestration (LangChain)
  - 2.5.3.1. LangChain Retrieval Chain
  - 2.5.3.2. Kết nối retriever → prompt → LLM → output

2.6. Đạo đức nghiên cứu & Trách nhiệm AI
2.6.1. Bảo mật & Quyền riêng tư dữ liệu (Data Privacy & Security)
- 2.6.1.1. Thu thập dữ liệu người dùng
  - Loại dữ liệu được thu thập: câu hỏi, hành vi truy vấn, metadata phiên
  - Cơ sở pháp lý: Nguyên tắc đồng ý (consent), ẩn danh hóa khi cần thiết
  - Không thu thập thông tin cá nhân nhạy cảm (họ tên, số điện thoại, email)
- 2.6.1.2. Lưu trữ và xử lý dữ liệu
  - Nơi lưu trữ: Local (Chromadb) + Cloud (OpenAI API logs)
  - Chính sách giữ lại: Không lưu trữ lịch sử hội thoại dài hạn
  - Mã hóa dữ liệu trong quá trình truyền tải (HTTPS)
- 2.6.1.3. Tuân thủ quy định
  - Nguyên tắc minimize: Chỉ thu thập dữ liệu cần thiết
  - Purpose limitation: Dữ liệu chỉ dùng để cải thiện trải nghiệm tư vấn
  - Tuân thủ các quy định bảo vệ dữ liệu cá nhân tại Việt Nam

2.6.2. Sự công bằng & Giảm thiểu thiên lệch (Fairness & Bias Mitigation)
- 2.6.2.1. Thiên lệch trong dữ liệu đào tạo (nguồn)
  - Kiểm tra tài liệu nguồn `data/sources/` có chứa thông tin thiên lệch không
  - Đảm bảo thông tin cân bằng giữa các ngành/nhóm đối tượng
  - Không phân biệt đối xử theo giới tính, dân tộc, khu vực
- 2.6.2.2. Thiên lệch trong phản hồi của LLM
  - Giám sát câu trả lời không chứa ngôn ngữ phân biệt đối xử
  - Chiến lược giảm thiểu: Prompt constraints, content filtering
- 2.6.2.3. Kiểm thử công bằng (Fairness Testing)
  - Đánh giá phản hồi với các nhóm đối tượng khác nhau
  - Test cases cho các nhóm: học sinh trường công/lập, nam/nữ, các vùng miền

2.6.3. Minh bạch & Giải thích được (Transparency & Explainability)
- 2.6.3.1. Minh bạch với người dùng
  - Thông báo rõ ràng người dùng đang tương tác với AI chatbot
  - Hiển thị nguồn thông tin trong câu trả lời (cited sources)
  - Thông báo đây là hệ thống tư vấn tự động, không thay thế tư vấn con người
- 2.6.3.2. Giải thích quyết định của hệ thống
  - Khả năng truy xuất tài liệu gốc đã dùng để trả lời
  - Ghi log quá trình RAG: retrieval → augmentation → generation
  - Cho phép người dùng xem context được sử dụnga
- 2.6.3.3. Ranh giới của hệ thống (System Boundaries)
  - Thông báo rõ khi nào hệ thống không biết / không chắc chắn
  - Cơ chế từ chối trả lời khi câu hỏi ngoài phạm vi
  - Tự động chuyển sang tư vấn con người khi cần (escalation)

2.6.4. Trách nhiệm & An toàn (Safety & Accountability)
- 2.6.4.1. Ngăn chặn thông tin sai lệch (Misinformation Prevention)
  - Cơ chế factual grounding: LLM chỉ trả lời dựa trên context được cung cấp
  - Xử lý hallucination: Câu hỏi không có trong tài liệu → từ chối trả lời
  - Kiểm tra độ chính xác thông tin trong tài liệu nguồn trước khi ingest
- 2.6.4.2. An toàn nội dung (Content Safety)
  - Bộ lọc nội dung không phù hợp (OpenAI content policy)
  - Giới hạn phạm vi câu hỏi được phép (chỉ về tuyển sinh, đào tạo)
  - Ngăn chặn prompt injection / jailbreaking
- 2.6.4.3. Phân công trách nhiệm (Accountability)
  - Ai chịu trách nhiệm khi chatbot đưa ra tư vấn sai?
  - Quy trình  xử lý khiếu nại / phản hồi từ người dùng
  - Cam kết của đơn vị phát triển về chất lượng thông tin
  - Khuyến cáo người dùng kiểm chứng thông tin quan trọng với nguồn chính thức

2.6.5. Toàn vẹn học thuật (Academic Integrity)
- 2.6.5.1. Trích dẫn nguồn
  - Trích dẫn đúng tài liệu tham khảo đã sử dụng trong báo cáo
  - Ghi nhận các công cụ và thư viện mã nguồn mở (LangChain, ChromaDB, OpenAI)
  - Ghi nhận Duy Tan University là đơn vị cung cấp dữ liệu
- 2.6.5.2. Sở hữu trí tuệ & Giấy phép
  - Giấy phép sử dụng của dữ liệu đầu vào
  - Giấy phép phát hành mã nguồn (MIT License) 
  - Tuân thủ điều khoản sử dụng OpenAI API

2.6.6. Tác động xã hội (Societal Impact)
- 2.6.6.1. Ảnh hưởng đến nghề nghiệp tư vấn tuyển sinh
  - Hỗ trợ, không thay thế hoàn toàn nhân viên tư vấn
  - Giải phóng thời gian cho các câu hỏi lặp đi lặp lại
  - Nâng cao chất lượng tư vấn (nhân viên tập trung vào cases phức tạp)
- 2.6.6.2. Đảm bảo tiếp cận công bằng (Accessibility)
  - Chi phí sử dụng thấp → tiếp cận nhiều đối tượng hơn
  - Hỗ trợ tiếng Việt → phù hợp với đại đa số thí sinh
  - Giao diện đơn giản, dễ sử dụng
- 2.6.6.3. Cam kết sử dụng đúng mục đích
  - Không sử dụng cho mục đích thương mại trái phép
  - Không sử dụng để lan truyền thông tin sai lệch
  - Cam kết cập nhật thông tin định kỳ

2.7. Triển khai hệ thống (System Implementation)
- 2.7.1. Công nghệ sử dụng (Tech Stack)
  - Ngôn ngữ lập trình: Python 3.13+
  - Framework: LangChain
  - Vector DB: ChromaDB
  - LLM & Embedding: OpenAI GPT-4o-mini, text-embedding-3-small
  - Quản lý cấu hình: Pydantic (BaseSettings)
  - Quản lý môi trường: python-dotenv
- 2.7.2. Cấu trúc thư mục dự án






  Duy-Tan-Chatbox/
  ├── src/
  │   ├── ingest/
  │   │   ├── loader.py         # MarkdownLoader
  │   │   ├── chunker.py        # DocumentChunker
  │   │   └── vectorstore.py     # VectorStoreManager
  │   ├── agent/
  │   │   ├── retriever.py      # AdmissionRetriever
  │   │   ├── chatbot.py         # AdmissionChatbot
  │   │   └── prompts.py         # Prompt templates
  │   ├── config/
  │   │   └── settings.py        # Pydantic Settings
  │   └── utils/
  │       └── logger.py          # Logging utilities
  ├── data/
  │   ├── sources/               # Markdown input files
  │   └── chromadb/              # Vector store output
  ├── tests/
  │   ├── playbook.csv           # Test questions & expected answers
  │   └── answerbook.csv         # Evaluation results
  ├── .env                        # Configuration (API keys, etc.)
  └── run_ingest.py               # Ingestion pipeline entry point
- 2.7.3. Quản lý cấu hình (Configuration Management)
  - Cấu hình tập trung trong `src/config/settings.py`
  - Load từ file `.env`
  - Các tham số: OpenAI API key, model names, paths, collection name
- 2.7.4. Pipeline xử lý (Processing Pipeline)
  - 2.7.4.1. Data Ingestion Pipeline
    - Load markdown → Chunk → Embed → Store
    - Điều phối bởi `run_ingest.py`
  - 2.7.4.2. Query Pipeline
    - User query → Embed → Retrieve → Augment → Generate → Response
    - Điều phối bởi `AdmissionChatbot`
- 2.7.5. Xử lý lỗi và ngoại lệ (Error Handling)
  - Kiểm tra tài liệu nguồn trước khi ingest
  - Fallback khi không tìm thấy tài liệu liên quan
  - Retry mechanism cho API calls
  - Graceful degradation khi LLM không phản hồi




PHẦN 3: THỰC NGHIỆM & KẾT QUẢ

3.1. Môi trường thực nghiệm
- 3.1.1. Cấu hình phần cứng / phần mềm thử nghiệm
  Hệ thống được triển khai và thử nghiệm trên môi trường phần mềm tối ưu cho các tác vụ xử lý ngôn ngữ tự nhiên hiện đại. Bảng 3.1 chi tiết các tham số cấu hình hệ thống.

  **Bảng 3.1 — Cấu hình môi trường thử nghiệm**

| Thành phần | Mô tả |
| :--- | :--- |
| Ngôn ngữ lập trình | Python 3.13+ |
| Framework RAG | LangChain 0.3.x |
| Vector Database | ChromaDB (persistent, collection: `admission_data`) |
| Embedding Model | `text-embedding-3-small` (1536 chiều) |
| LLM | `gpt-4o-mini`, temperature = 0 |
| Nguồn dữ liệu | Markdown files tại `data/sources/` |
| Kho lưu trữ vector | `data/chromadb/` |
| Chunk size | 1000 ký tự, overlap 100 ký tự |
| Số lượng document (k) | Top 5 |

- 3.1.2. Bộ dữ liệu kiểm thử (Test Dataset)
  - 3.1.2.1. Nguồn test cases
    Hệ thống được đánh giá dựa trên bộ dữ liệu kiểm thử gồm 18 kịch bản (test cases) đa dạng, lưu trữ tại `tests/testcase.csv`. Phân bổ các nhóm câu hỏi được chi tiết trong Bảng 3.2.

    **Bảng 3.2 — Phân bổ bộ dữ liệu kiểm thử**

| Nhóm câu hỏi | Số lượng | Tỷ lệ | Nội dung trọng tâm |
| :--- | :---: | :---: | :--- |
| **Admission** | 13 | 72.2% | Thông tin ngành, chuyên ngành, mã tuyển sinh. |
| **Out-of-scope** | 2 | 11.1% | Kiểm tra khả năng từ chối các câu hỏi ngoài ngành. |
| **Edge-case** | 2 | 11.1% | Câu hỏi thiếu từ khóa hoặc cấu trúc phức tạp. |
| **Scholarship** | 1 | 5.6% | Chính sách học bổng và hỗ trợ học phí. |
| **Tổng cộng** | **18** | **100%** | |
  - 3.1.2.2. Cấu trúc testcase
    Mỗi trường hợp kiểm thử được cấu trúc chặt chẽ gồm: `ID`, `Test_Category` (phân loại), `Input` (câu hỏi của người dùng), `Target` (câu trả lời chuẩn từ tài liệu gốc), `Expected Behavior` (hành vi kỳ vọng) và `Priority` (mức độ ưu tiên).

- 3.1.3. Phương pháp đánh giá
  - 3.1.3.1. Cosine Similarity
    Sử dụng kỹ thuật so sánh vector để đo lường độ tương đồng ngữ nghĩa giữa câu trả lời của Chatbot (Output) và câu trả lời mẫu (Target). Cả hai được chuyển đổi sang không gian vector bằng mô hình `text-embedding-3-small`.
  - 3.1.3.2. Các metric bổ sung
    Dựa trên kết quả thực nghiệm, hệ thống phân loại chất lượng câu trả lời theo các ngưỡng điểm:
    - **TỐT (Score ≥ 0.75):** Câu trả lời phản ánh chính xác và đầy đủ thông tin từ ngữ cảnh.
    - **TRUNG BÌNH (0.65 ≤ Score < 0.75):** Câu trả lời đúng trọng tâm nhưng có thể thiếu một vài ý phụ hoặc cách diễn đạt chưa tối ưu.
    - **THẤP (Score < 0.65):** Câu trả lời bị sai lệch thông tin hoặc gặp hiện tượng "hallucination".

3.2. Kết quả thực nghiệm
- 3.2.1. Chất lượng trả lời (Answer Quality)
  - 3.2.1.1. Điểm similarity trung bình
  - 3.2.1.2. Phân tích chi tiết theo từng câu hỏi
  - 3.2.1.3. Phân tích theo loại câu hỏi
    - Câu hỏi về ngành học
    - Câu hỏi về điểm chuẩn / tiêu chí tuyển sinh
    - Câu hỏi về học phí / học bổng
    - Câu hỏi về cơ hội nghề nghiệp
    - Câu hỏi ngoài phạm vi
- 3.2.2. Hiệu suất truy xuất (Retrieval Performance)
  - 3.2.2.1. Độ chính xác của việc tìm kiếm tài liệu liên quan
  - 3.2.2.2. Ảnh hưởng của tham số k (thử nghiệm k=3, k=5, k=10)
  - 3.2.2.3. Chất lượng chunking (đánh giá segmentation)
- 3.2.3. Chất lượng ngôn ngữ tiếng Việt
  - 3.2.3.1. Độ tự nhiên của câu trả lời tiếng Việt
  - 3.2.3.2. Độ chính xác thuật ngữ chuyên ngành
- 3.2.4. Xử lý các trường hợp ngoài phạm vi (Out-of-scope Handling)
  - 3.2.4.1. Tỷ lệ từ chối trả lời đúng khi câu hỏi ngoài phạm vi
  - 3.2.4.2. Chất lượng câu trả lời thay thế ("Tôi không biết câu trả lời...")

3.3. Phân tích & Đánh giá
- 3.3.1. Đánh giá tổng thể hệ thống
  - Điểm mạnh: Độ chính xác cao khi câu hỏi trong phạm vi tài liệu
  - Điểm yếu: Hạn chế khi xử lý câu hỏi phức tạp, đa ngữ cảnh
- 3.3.2. So sánh với các phương pháp khác (Baseline Comparison)
  - So sánh với GPT-4o-mini không có RAG (zero-shot)
  - So sánh với keyword search thuần túy
  - So sánh với các chiến lược chunking khác
- 3.3.3. Phân tích lỗi và hạn chế
  - 3.3.3.1. Retrieval failure cases
    - Chunk quá nhỏ → thiếu context
    - Chunk quá lớn → nhiễu thông tin
  - 3.3.3.2. Generation failure cases
    - Hallucination khi context không đầy đủ
    - Câu trả lời không đầy đủ cho câu hỏi đòi hỏi tổng hợp nhiều nguồn
  - 3.3.3.3. Hạn chế về ngôn ngữ
    - Một số thuật ngữ tiếng Việt chuyên ngành chưa được xử lý tốt

3.4. Kết luận & Hướng phát triển
- 3.4.1. Tổng kết kết quả đạt được
  - So sánh với mục tiêu ban đầu (mục 1.4)
  - Các mục tiêu đã đạt được
  - Các mục tiêu chưa đạt được và lý do
- 3.4.2. Đóng góp của nghiên cứu
  - Đóng góp về mặt kỹ thuật: Kiến trúc RAG cho tư vấn tuyển sinh
  - Đóng góp về mặt thực tiễn: Giải pháp tự động hóa tư vấn
  - Đóng góp về mặt học thuật: Tài liệu tham khảo cho các nghiên cứu tiếp theo
- 3.4.3. Hạn chế của hệ thống
  - Phụ thuộc vào chất lượng tài liệu nguồn
  - Chi phí API OpenAI
  - Giới hạn ngôn ngữ (chỉ tiếng Việt)
  - Không hỗ trợ tư vấn cá nhân hóa (theo profile từng học sinh)
- 3.4.4. Hướng nghiên cứu tương lai
  - 3.4.4.1. Cải thiện độ chính xác truy xuất
    - Thử nghiệm mô hình embedding chuyên biệt cho tiếng Việt
    - Hybrid search (kết hợp semantic + keyword)
    - Reranking documents sau retrieval
  - 3.4.4.2. Mở rộng ngôn ngữ & phạm vi
    - Hỗ trợ tiếng Anh, Trung
    - Mở rộng sang các ngành khác ngoài CS & AI
    - Tích hợp thông tin tuyển sinh theo năm
  - 3.4.4.3. Tích hợp feedback loop
    - Thu thập phản hồi từ người dùng
    - Cập nhật tài liệu nguồn tự động
    - Fine-tuning LLM dựa trên feedback
  - 3.4.4.4. Các cải tiến khác
    - Hỗ trợ tư vấn cá nhân hóa (dựa trên điểm số, sở thích)
    - Tích hợp chatbot vào website / ứng dụng di động
    - Multi-turn conversation (hỏi đáp liên tiếp)

TÀI LIỆU THAM KHẢO


---

*Lưu ý: Đây là khung sườn báo cáo. Các số liệu, kết quả thực nghiệm, và nội dung chi tiết cần được điền bổ sung trong quá trình hoàn thiện bài báo cáo.*
