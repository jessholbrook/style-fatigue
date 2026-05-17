import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useParticipant } from "../hooks/useParticipant";
import { useSession } from "../hooks/useSession";
import {
  startConversation,
  sendMessage as sendMessageApi,
  getIntents,
} from "../api/client";
import type { Conversation, Message } from "../types";
import IntentPicker from "../components/IntentPicker";
import ChatWindow from "../components/ChatWindow";
import { Button } from "@/components/ui/button";

const MAX_TURNS = 5;

export default function ChatPage() {
  const { participant, token, loading: pLoading, error: pError } = useParticipant();
  const { session, loading: sLoading, error: sError, begin } = useSession(token);
  const navigate = useNavigate();

  const [phase, setPhase] = useState<"loading" | "pick-intent" | "chat" | "done">("loading");
  const [intents, setIntents] = useState<Array<{ slug: string; label: string; topics: string[] }>>([]);
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [sending, setSending] = useState(false);

  useEffect(() => {
    if (!participant || !participant.consent_given_at) return;
    begin().then((s) => {
      if (s) {
        getIntents().then((data) => {
          setIntents(data.intents);
          setPhase("pick-intent");
        });
      }
    });
  }, [participant?.id]);

  if (pLoading || sLoading) return <p className="text-muted-foreground">Loading...</p>;
  if (pError || sError) return <p className="text-destructive">Error: {pError || sError}</p>;
  if (!participant?.consent_given_at) {
    navigate(`/${token}/consent`);
    return null;
  }

  async function handleIntentSelect(intent: string, topic: string) {
    if (!session) return;
    const conv = await startConversation(session.id, intent, topic);
    setConversation(conv);
    setMessages(conv.messages);
    setPhase("chat");
  }

  async function handleSend(content: string) {
    if (!session || !conversation) return;
    setSending(true);
    try {
      const updated = await sendMessageApi(session.id, conversation.id, content);
      setConversation(updated);
      setMessages(updated.messages);
      if (updated.turn_count >= MAX_TURNS) {
        setPhase("done");
      }
    } finally {
      setSending(false);
    }
  }

  if (phase === "pick-intent") {
    return <IntentPicker intents={intents} onSelect={handleIntentSelect} />;
  }

  if (phase === "chat" || phase === "done") {
    return (
      <div>
        <ChatWindow
          messages={messages}
          onSend={handleSend}
          disabled={phase === "done"}
          loading={sending}
          maxTurns={MAX_TURNS}
          currentTurns={conversation?.turn_count ?? 0}
        />
        {phase === "done" && (
          <div className="text-center mt-6 space-y-4">
            <p className="text-muted-foreground">Conversation complete. Please continue to the survey.</p>
            <Button onClick={() => navigate(`/${token}/survey`)}>
              Continue to Survey
            </Button>
          </div>
        )}
      </div>
    );
  }

  return <p className="text-muted-foreground">Setting up your session...</p>;
}
