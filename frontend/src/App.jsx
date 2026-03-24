import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { 
      role: "bot", 
      text: "DTU – Trợ lý AI Chatbot xin chào bạn! \nBạn đang kết nối với DTU Admission AI Chatbot - nền tảng sử dụng trí tuệ nhân tạo trong tuyển sinh và hướng nghiệp. Nếu có thắc mắc về ngành học, học bổng … đừng ngần ngại đặt câu hỏi để được hỗ trợ ngay nhé!" 
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const chatWindowRef = useRef(null);

  // Tự động cuộn xuống khi có tin nhắn mới
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages, isLoading, isOpen]);

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

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullAnswer = "";
      let hasAddedBotMessage = false;
      let buffer = ""; // Buffer để lưu dữ liệu chưa hoàn chỉnh

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        
        // Chia buffer thành các dòng
        let lines = buffer.split("\n");
        // Giữ lại dòng cuối cùng (có thể chưa hoàn chỉnh) vào buffer
        buffer = lines.pop();

        for (const line of lines) {
          const trimmedLine = line.trim();
          if (!trimmedLine || !trimmedLine.startsWith("data: ")) continue;

          const dataStr = trimmedLine.slice(6);
          if (dataStr === "[DONE]") break;

          try {
            const data = JSON.parse(dataStr);
            if (data.token) {
              fullAnswer += data.token;
              
              if (!hasAddedBotMessage) {
                setMessages(prev => [...prev, { role: "bot", text: fullAnswer }]);
                hasAddedBotMessage = true;
              } else {
                setMessages(prev => {
                  const newMessages = [...prev];
                  newMessages[newMessages.length - 1] = { 
                    role: "bot", 
                    text: fullAnswer 
                  };
                  return newMessages;
                });
              }
            }
          } catch (e) {
            console.error("Error parsing JSON chunk:", dataStr, e);
          }
        }
      }

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
    <div className="app-wrapper">
      {/* Nút bong bóng chat khi đóng */}
      {!isOpen && (
        <div className="chat-bubble-container" onClick={() => setIsOpen(true)}>
          <div className="chat-bubble-label">DUY-Tư vấn tuyển sinh</div>
          <div className="chat-bubble-icon">
            <div className="bot-avatar-large">DT</div>
          </div>
        </div>
      )}

      {/* Cửa sổ chat khi mở */}
      {isOpen && (
        <div className="chat-container">
          <header className="chat-header">
            <div className="header-info">
              <div className="bot-avatar">DT</div>
              <div className="header-text">
                <h1>DTU - Trợ lý ảo Tư vấn Tuyển sinh</h1>
                <p className="status">Trực tuyến</p>
              </div>
              <button className="close-btn" onClick={() => setIsOpen(false)}>
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
              </button>
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
      )}
    </div>
  )
}

export default App
