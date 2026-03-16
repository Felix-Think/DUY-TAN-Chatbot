import { useState } from 'react'
import './App.css'

function App() {
  // State : Nơi lưu trữ tin nhắn và nội dung đang nhập
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { role: "bot", text: "Chào bạn! Mình là trợ lý tuyển sinh Duy Tân. Bạn càn hỏi gì không? " }
  ]);
  // Hàm xử lý khi nhấn nút gửi
  const handleSend = () => {
    if (!input.trim()) return;
    // Thêm tín nhắn người dùng vào danh sách
    const userMessages = { role: "user", text: input };
    setMessages([...messages, userMessages]);
    // Sau đó xóa thông tin ô nhập liệu
    setInput("");
  };
  return (
    <div className="chat-container">
      <h1> Duy Tan Admission Chatbot</h1>
      {
        /* Vùng hiển thị tin nhắn */
      }
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`messages ${msg.role}`}>
            {msg.text}
          </div>
        ))}
      </div>
      { /* Vùng nhập liệu */}
      <div className="input-area">
        <input
          type="text"
          value={input}
          onchange={(e) => setInput(e.target.value)} // Cập nhật khi gõ phím
          placeholder="Nhập câu hỏi của bạn..."
        />
      </div>
      <button onClick={handleSend}>Gửi</button>
    </div>

  )


}
export default App
