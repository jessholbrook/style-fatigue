import { useState, useRef, useEffect } from "react";
import type { Message } from "../types";
import MessageBubble from "./MessageBubble";

interface Props {
  messages: Message[];
  onSend: (content: string) => void;
  disabled: boolean;
  loading: boolean;
  maxTurns: number;
  currentTurns: number;
}

export default function ChatWindow({
  messages,
  onSend,
  disabled,
  loading,
  maxTurns,
  currentTurns,
}: Props) {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || disabled || loading) return;
    onSend(input.trim());
    setInput("");
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "1rem 0",
          minHeight: "300px",
        }}
      >
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        {loading && (
          <div style={{ color: "var(--color-text-secondary)", padding: "0.5rem" }}>
            Thinking...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div style={{ padding: "0.5rem 0", color: "var(--color-text-secondary)", fontSize: "0.875rem" }}>
        Turn {currentTurns} of {maxTurns}
      </div>

      <form onSubmit={handleSubmit} style={{ display: "flex", gap: "0.5rem" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={disabled ? "Conversation complete" : "Type your message..."}
          disabled={disabled || loading}
          style={{
            flex: 1,
            padding: "0.75rem",
            border: "1px solid var(--color-border)",
            borderRadius: "var(--radius)",
            outline: "none",
          }}
        />
        <button
          type="submit"
          disabled={disabled || loading || !input.trim()}
          style={{
            padding: "0.75rem 1.5rem",
            backgroundColor: "var(--color-primary)",
            color: "white",
            border: "none",
            borderRadius: "var(--radius)",
            opacity: disabled || loading || !input.trim() ? 0.5 : 1,
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
}
