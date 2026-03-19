import { useState } from 'react'
import './App.css'

function App() {
  // State: Nơi lưu trữ tin nhắn và nội dung đang nhập
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { role: "bot", text: "Chào bạn! Mình là trợ lý tuyển sinh Duy Tân. Bạn cần hỏi gì không?" }
  ]);
  const [isLoading, setIsLoading] = useState(false); // Trạng thái "Đang đợi phản hồi" từ AI

  // Hàm xử lý khi nhấn nút Gửi hoặc phím Enter
  const handleSend = async () => {
    // Không gửi nếu ô nhập trống hoặc đang trong quá trình chờ phản hồi
    if (!input.trim() || isLoading) return;

    // 1. Thêm tin nhắn của người dùng vào danh sách hiển thị
    const userMessage = { role: "user", text: input };
    setMessages(prev => [...prev, userMessage]);

    // Xóa nội dung ô nhập và bật trạng thái đang tải
    const currentInput = input;
    setInput("");
    setIsLoading(true);
    const default_secret_key = "duytan-secret-2024"
    // Lấy URL API từ biến môi trường, mặc định là localhost nếu không có
    const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
    
    try {
      // 2. Gửi yêu cầu đến Backend Python (FastAPI)
      const response = await fetch(`${API_BASE_URL}/api/v1/chat/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-KEY": default_secret_key
        },
        body: JSON.stringify({ query: currentInput })
      });

      if (!response.ok) {
        throw new Error("Lỗi từ server");
      }

      const data = await response.json();

      // 3. Cập nhật câu trả lời từ AI vào danh sách tin nhắn
      // 'data.answer' là trường dữ liệu mà Backend của bạn trả về
      setMessages(prev => [...prev, { role: "bot", text: data.answer }]);

    } catch (error) {
      console.error("Lỗi kết nối:", error);
      setMessages(prev => [...prev, {
        role: "bot",
        text: "Rất tiếc, mình đang gặp sự cố kết nối với máy chủ. Bạn vui lòng thử lại sau nhé!"
      }]);
    } finally {
      setIsLoading(false); // Tắt trạng thái đang tải
    }
  };

  return (
    <div className="chat-container">
      {/* Tiêu đề ứng dụng */}
      <h1>Duy Tân Admission Chatbot</h1>

      {/* Vùng hiển thị nội dung hội thoại */}
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            {msg.text}
          </div>
        ))}

        {/* Hiển thị hiệu ứng chờ khi AI đang suy nghĩ */}
        {isLoading && (
          <div className="message bot italic">
            Đang tìm kiếm thông tin...
          </div>
        )}
      </div>

      {/* Vùng nhập liệu và nút gửi */}
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()} // Gửi nhanh bằng phím Enter
          placeholder="Bạn muốn hỏi gì về tuyển sinh Duy Tân?"
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading}>
          {isLoading ? "..." : "Gửi"}
        </button>
      </div>
    </div>
  )
}

export default App
