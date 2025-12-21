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
      const response = await fetch("https://ai-native-book-website.onrender.com", {
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
          background: "#171717",
          color: "white",
          border: "1px solid #262626",
          fontSize: "28px",
          cursor: "pointer",
          boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
          zIndex: 1000,
          transition: "all 0.2s ease",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: 0,
          overflow: "hidden",
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = "#262626";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "#171717";
        }}
      >
        <img
          src="/bot.jpg"
          alt="Chat Bot"
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            borderRadius: "50%",
          }}
        />
      </button>

      {open && (
        <div
          style={{
            position: "fixed",
            bottom: "100px",
            right: "30px",
            width: "380px",
            height: "550px",
            background: "#ffffff",
            borderRadius: "12px",
            boxShadow: "0 10px 30px rgba(0,0,0,0.15)",
            display: "flex",
            flexDirection: "column",
            zIndex: 1000,
            border: "1px solid #e5e5e5",
          }}
        >
          <div
            style={{
              padding: "16px",
              background: "#171717",
              color: "#ffffff",
              borderTopLeftRadius: "12px",
              borderTopRightRadius: "12px",
              fontWeight: "600",
              display: "flex",
              justifyContent: "space-between",
              borderBottom: "1px solid #262626",
            }}
          >
            Book Assistant
            <button
              onClick={() => setOpen(false)}
              style={{
                background: "none",
                border: "none",
                color: "#ffffff",
                fontSize: "20px",
                cursor: "pointer",
                transition: "opacity 0.2s",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.opacity = "0.7";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.opacity = "1";
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
              background: "#fafafa",
            }}
          >
            {messages.length === 0 && (
              <div style={{ color: "#737373", fontStyle: "italic", fontSize: "14px" }}>
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
                    background: msg.role === "user" ? "#171717" : "#ffffff",
                    color: msg.role === "user" ? "#ffffff" : "#171717",
                    border:
                      msg.role === "assistant" ? "1px solid #e5e5e5" : "1px solid #171717",
                    maxWidth: "80%",
                    whiteSpace: "pre-wrap",
                    fontSize: "14px",
                    lineHeight: "1.5",
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
              borderTop: "1px solid #e5e5e5",
              background: "#ffffff",
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
                padding: "10px 14px",
                borderRadius: "20px",
                border: "1px solid #d4d4d4",
                fontSize: "14px",
                outline: "none",
                transition: "border-color 0.2s",
              }}
              onFocus={(e) => {
                e.currentTarget.style.borderColor = "#737373";
              }}
              onBlur={(e) => {
                e.currentTarget.style.borderColor = "#d4d4d4";
              }}
            />
            <button
              onClick={sendMessage}
              disabled={loading}
              style={{
                marginLeft: "8px",
                padding: "10px 16px",
                background: "#171717",
                color: "#ffffff",
                border: "1px solid #171717",
                borderRadius: "20px",
                cursor: loading ? "not-allowed" : "pointer",
                fontSize: "14px",
                fontWeight: "500",
                transition: "all 0.2s",
                opacity: loading ? 0.5 : 1,
              }}
              onMouseEnter={(e) => {
                if (!loading) {
                  e.currentTarget.style.background = "#262626";
                }
              }}
              onMouseLeave={(e) => {
                if (!loading) {
                  e.currentTarget.style.background = "#171717";
                }
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
