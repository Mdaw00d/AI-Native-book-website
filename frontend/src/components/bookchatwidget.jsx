import React, { useState } from "react";

export default function BookChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMsg = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);   

    // Add placeholder for assistant response
    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    try {
      const response = await fetch("https://padh-book.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantContent = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        assistantContent += chunk;

        // Update the last message with new content
        setMessages((prev) => {
          const newMsgs = [...prev];
          newMsgs[newMsgs.length - 1].content = assistantContent;
          return newMsgs;
        });
      }
    } catch (err) {
      setMessages((prev) => {
        const newMsgs = [...prev];
        newMsgs[newMsgs.length - 1].content = `Error: ${err.message}`;
        return newMsgs;
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button
        onClick={() => setOpen(!open)}
        style={{
          position: "fixed",
          bottom: "30px",
          right: "30px",
          width: "60px",
          height: "60px",
          borderRadius: "50%",
          background: "#1a56db",
          color: "white",
          border: "none",
          fontSize: "28px",
          cursor: "pointer",
          boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
          zIndex: 1000,
        }}
      >
        💬
      </button>

      {open && (
        <div
          style={{
            position: "fixed",
            bottom: "100px",
            right: "30px",
            width: "380px",
            height: "550px",
            background: "white",
            borderRadius: "12px",
            boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
            display: "flex",
            flexDirection: "column",
            zIndex: 1000,
            border: "1px solid #e5e7eb",
          }}
        >
          <div
            style={{
              padding: "16px",
              background: "#1a56db",
              color: "white",
              borderTopLeftRadius: "12px",
              borderTopRightRadius: "12px",
              fontWeight: "bold",
              display: "flex",
              justifyContent: "space-between",
            }}
          >
            Book Assistant
            <button
              onClick={() => setOpen(false)}
              style={{
                background: "none",
                border: "none",
                color: "white",
                fontSize: "20px",
                cursor: "pointer",
              }}
            >
              ✕
            </button>
          </div>

          <div
            style={{
              flex: 1,
              padding: "16px",
              overflowY: "auto",
              background: "#f9fafb",
            }}
          >
            {messages.length === 0 && (
              <div style={{ color: "#666", fontStyle: "italic" }}>
                Ask me anything about the book!
              </div>
            )}
            {messages.map((msg, i) => (
              <div
                key={i}
                style={{
                  marginBottom: "12px",
                  textAlign: msg.role === "user" ? "right" : "left",
                }}
              >
                <span
                  style={{
                    display: "inline-block",
                    padding: "10px 14px",
                    borderRadius: "18px",
                    background: msg.role === "user" ? "#1a56db" : "white",
                    color: msg.role === "user" ? "white" : "black",
                    border:
                      msg.role === "assistant" ? "1px solid #e5e7eb" : "none",
                    maxWidth: "80%",
                    whiteSpace: "pre-wrap",
                  }}
                >
                  {msg.content ||
                    (loading &&
                    msg.role === "assistant" &&
                    i === messages.length - 1
                      ? "Thinking..."
                      : "")}
                </span>
              </div>
            ))}
          </div>

          <div
            style={{
              padding: "12px",
              borderTop: "1px solid #e5e7eb",
              background: "white",
            }}
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder="Ask about the book..."
              disabled={loading}
              style={{
                width: "78%",
                padding: "10px",
                borderRadius: "20px",
                border: "1px solid #ccc",
              }}
            />
            <button
              onClick={sendMessage}
              disabled={loading}
              style={{
                marginLeft: "8px",
                padding: "10px 16px",
                background: "#1a56db",
                color: "white",
                border: "none",
                borderRadius: "20px",
                cursor: "pointer",
              }}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
}
