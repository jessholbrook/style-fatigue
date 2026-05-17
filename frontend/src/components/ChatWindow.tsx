import { useState, useRef, useEffect } from "react";
import type { Message } from "../types";
import MessageBubble from "./MessageBubble";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

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
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto py-4 min-h-[300px]">
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        {loading && (
          <div className="text-muted-foreground px-2 py-1 text-sm">
            Thinking...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="py-2 text-sm text-muted-foreground">
        Turn {currentTurns} of {maxTurns}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={disabled ? "Conversation complete" : "Type your message..."}
          disabled={disabled || loading}
        />
        <Button
          type="submit"
          disabled={disabled || loading || !input.trim()}
        >
          Send
        </Button>
      </form>
    </div>
  );
}
