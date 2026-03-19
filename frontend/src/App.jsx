import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { role: "bot", text: "Chào bạn! Mình là trợ lý tuyển sinh Duy Tân. Bạn cần hỏi gì không?" }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const chatWindowRef = useRef(null);

  // Tự động cuộn xuống khi có tin nhắn mới
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: "user", text: input };
    setMessages(prev => [...prev, userMessage]);

    const currentInput = input;
    setInput("");
    setIsLoading(true);
    const default_secret_key = "duytan-secret-2024"
    const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
    
    try {
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
      setMessages(prev => [...prev, { role: "bot", text: data.answer }]);

    } catch (error) {
      console.error("Lỗi kết nối:", error);
      setMessages(prev => [...prev, {
        role: "bot",
        text: "**Rất tiếc**, mình đang gặp sự cố kết nối với máy chủ. Bạn vui lòng thử lại sau nhé!"
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <div className="header-info">
          <div className="bot-avatar">DT</div>
          <div>
            <h1>Duy Tân Chatbot</h1>
            <p className="status">Trực tuyến</p>
          </div>
        </div>
      </header>

      <div className="chat-window" ref={chatWindowRef}>
        {messages.map((msg, index) => (
          <div key={index} className={`message-row ${msg.role}`}>
            <div className="message-bubble">
              {msg.role === "bot" ? (
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              ) : (
                msg.text
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message-row bot">
            <div className="message-bubble loading">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </div>
          </div>
        )}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Nhập câu hỏi của bạn..."
          disabled={isLoading}
        />
        <button className="send-btn" onClick={handleSend} disabled={isLoading || !input.trim()}>
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
        </button>
      </div>
    </div>
  )
}

export default App
