import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useParticipant } from "../hooks/useParticipant";
import { getSurveyInstrument, submitSurvey } from "../api/client";
import type { SurveyQuestion } from "../types";
import SurveyForm from "../components/SurveyForm";

export default function SurveyPage() {
  const { token } = useParticipant();
  const navigate = useNavigate();
  const [questions, setQuestions] = useState<SurveyQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [sessionId, setSessionId] = useState<string | null>(null);

  useEffect(() => {
    getSurveyInstrument("post_conversation")
      .then((instrument) => setQuestions(instrument.questions))
      .finally(() => setLoading(false));

    const stored = sessionStorage.getItem("current_session_id");
    if (stored) setSessionId(stored);
  }, []);

  async function handleSubmit(responses: Record<string, unknown>, freeText?: string) {
    if (!sessionId) return;
    await submitSurvey(sessionId, "post_conversation", responses, freeText);
    navigate(`/${token}/complete`);
  }

  if (loading) return <p>Loading survey...</p>;

  return (
    <div>
      <h1 style={{ marginBottom: "0.5rem" }}>Post-Conversation Survey</h1>
      <p style={{ color: "var(--color-text-secondary)", marginBottom: "2rem" }}>
        Please answer the following questions about the conversation you just had.
      </p>
      <SurveyForm questions={questions} onSubmit={handleSubmit} />
    </div>
  );
}
