import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useParticipant } from "../hooks/useParticipant";
import { useSession } from "../hooks/useSession";
import {
  startConversation,
  sendMessage as sendMessageApi,
  getIntents,
  getConfig,
  logEvent,
  detailReason,
  ApiError,
} from "../api/client";
import type { Conversation, Message, IntentItem } from "../types";
import IntentPicker from "../components/IntentPicker";
import ChatWindow from "../components/ChatWindow";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type Phase =
  | "loading"
  | "pick-intent"
  | "chat"
  | "done"
  | "cooldown"
  | "expired"
  | "error";

export default function ChatPage() {
  const { participant, token, loading: pLoading, error: pError } = useParticipant();
  const { session, begin } = useSession(token);
  const navigate = useNavigate();

  const [phase, setPhase] = useState<Phase>("loading");
  const [intents, setIntents] = useState<IntentItem[]>([]);
  const [maxTurns, setMaxTurns] = useState(5);
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [sending, setSending] = useState(false);
  const [nextAvailableAt, setNextAvailableAt] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!participant) return;
    if (!participant.consent_given_at) {
      navigate(`/${token}/consent`);
      return;
    }

    let cancelled = false;
    (async () => {
      try {
        const [start, config, intentData] = await Promise.all([
          begin(),
          getConfig(),
          getIntents(token),
        ]);
        if (cancelled) return;

        setMaxTurns(config.turns_per_conversation.max);
        setIntents(intentData.intents);

        if (start.conversation) {
          setConversation(start.conversation);
          setMessages(start.conversation.messages);
          const finished =
            start.conversation.completed_at !== null ||
            start.conversation.turn_count >= config.turns_per_conversation.max;
          setPhase(finished ? "done" : "chat");
        } else {
          setPhase("pick-intent");
        }
      } catch (e) {
        if (cancelled) return;
        const reason = detailReason(e);
        if (reason === "cooldown") {
          setNextAvailableAt(
            (e as ApiError).detail && typeof (e as ApiError).detail === "object"
              ? ((e as ApiError).detail as { next_available_at?: string }).next_available_at ?? null
              : null
          );
          setPhase("cooldown");
        } else if (reason === "study_complete") {
          navigate(`/${token}/complete`);
        } else if (reason === "study_expired") {
          setPhase("expired");
        } else {
          setErrorMessage(e instanceof Error ? e.message : "Something went wrong");
          setPhase("error");
        }
      }
    })();
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [participant?.id]);

  if (pLoading) return <p className="text-muted-foreground">Loading...</p>;
  if (pError) return <p className="text-destructive">Invalid or expired study link.</p>;

  async function handleIntentSelect(intent: string, topic: string) {
    if (!session) return;
    const conv = await startConversation(token, session.id, intent, topic);
    setConversation(conv);
    setMessages(conv.messages);
    setPhase("chat");
  }

  async function handleSend(content: string) {
    if (!session || !conversation) return;
    setSending(true);
    try {
      const updated = await sendMessageApi(token, session.id, conversation.id, content);
      setConversation(updated);
      setMessages(updated.messages);
      logEvent(token, "response_rendered", { turn: updated.turn_count }, session.id);
      if (updated.completed_at !== null || updated.turn_count >= maxTurns) {
        setPhase("done");
      }
    } finally {
      setSending(false);
    }
  }

  if (phase === "cooldown") {
    const when = nextAvailableAt ? new Date(nextAvailableAt).toLocaleString() : "soon";
    return (
      <Card className="text-center">
        <CardHeader>
          <CardTitle>You're all set for now</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <p className="text-muted-foreground">
            Your next session isn't available yet — sessions are spaced out over the study.
          </p>
          <p>
            Please come back after <strong>{when}</strong> using this same link.
          </p>
        </CardContent>
      </Card>
    );
  }

  if (phase === "expired") {
    return (
      <Card className="text-center">
        <CardHeader>
          <CardTitle>Study period ended</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            The participation window for this study has closed. Thank you for your interest!
          </p>
        </CardContent>
      </Card>
    );
  }

  if (phase === "error") {
    return <p className="text-destructive">Error: {errorMessage}</p>;
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
          maxTurns={maxTurns}
          currentTurns={conversation?.turn_count ?? 0}
        />
        {phase === "done" && (
          <div className="text-center mt-6 space-y-4">
            <p className="text-muted-foreground">
              Conversation complete. Please continue to the survey.
            </p>
            <Button onClick={() => navigate(`/${token}/survey`)}>Continue to Survey</Button>
          </div>
        )}
      </div>
    );
  }

  return <p className="text-muted-foreground">Setting up your session...</p>;
}
