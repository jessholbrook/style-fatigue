import type { Message } from "../types";
import { cn } from "@/lib/utils";

export default function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";
  return (
    <div className={cn("flex mb-3", isUser ? "justify-end" : "justify-start")}>
      <div
        className={cn(
          "max-w-[80%] rounded-lg px-4 py-3 whitespace-pre-wrap text-sm",
          isUser ? "bg-user" : "bg-assistant"
        )}
      >
        {message.content}
      </div>
    </div>
  );
}
