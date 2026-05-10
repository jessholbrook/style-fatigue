import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useParticipant } from "../hooks/useParticipant";
import { recordConsent } from "../api/client";

export default function ConsentPage() {
  const { participant, token, loading, error } = useParticipant();
  const navigate = useNavigate();
  const [agreed, setAgreed] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  if (loading) return <p>Loading...</p>;
  if (error || !participant) return <p>Invalid or expired study link.</p>;

  if (participant.consent_given_at) {
    navigate(`/${token}/chat`);
    return null;
  }

  async function handleConsent() {
    setSubmitting(true);
    try {
      await recordConsent(token);
      navigate(`/${token}/chat`);
    } catch {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <h1 style={{ marginBottom: "1.5rem" }}>Informed Consent</h1>

      <div
        style={{
          border: "1px solid var(--color-border)",
          borderRadius: "var(--radius)",
          padding: "1.5rem",
          marginBottom: "1.5rem",
          maxHeight: "400px",
          overflowY: "auto",
          backgroundColor: "var(--color-surface)",
        }}
      >
        <h3>Study Purpose</h3>
        <p style={{ marginBottom: "1rem" }}>
          This research investigates how people interact with AI assistants over time,
          specifically how perceptions of AI communication style change across multiple
          conversations.
        </p>

        <h3>What You'll Do</h3>
        <p style={{ marginBottom: "1rem" }}>
          You'll complete 4-6 short sessions over approximately two weeks. Each session
          involves a brief conversation with an AI assistant followed by a short survey.
          Sessions take about 5-10 minutes each.
        </p>

        <h3>Data Collection</h3>
        <p style={{ marginBottom: "1rem" }}>
          We will record your conversations, survey responses, and interaction timing.
          No personally identifying information is collected. Your participation is
          identified only by a random token.
        </p>

        <h3>Risks & Benefits</h3>
        <p style={{ marginBottom: "1rem" }}>
          There are no known risks beyond those of normal computer use. You may
          withdraw at any time without penalty.
        </p>
      </div>

      <label style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "1.5rem" }}>
        <input
          type="checkbox"
          checked={agreed}
          onChange={(e) => setAgreed(e.target.checked)}
        />
        I have read and agree to participate in this study
      </label>

      <button
        onClick={handleConsent}
        disabled={!agreed || submitting}
        style={{
          padding: "0.75rem 2rem",
          backgroundColor: "var(--color-primary)",
          color: "white",
          border: "none",
          borderRadius: "var(--radius)",
          fontSize: "1rem",
          opacity: !agreed || submitting ? 0.5 : 1,
        }}
      >
        {submitting ? "Submitting..." : "I Agree — Begin Study"}
      </button>
    </div>
  );
}
