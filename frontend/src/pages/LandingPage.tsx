import { useNavigate } from "react-router-dom";
import { useParticipant } from "../hooks/useParticipant";

export default function LandingPage() {
  const { participant, token, loading, error } = useParticipant();
  const navigate = useNavigate();

  if (loading) return <p>Loading...</p>;
  if (error || !participant) return <p>Invalid or expired study link.</p>;

  return (
    <div>
      <h1 style={{ marginBottom: "1.5rem" }}>Welcome to the Study</h1>
      <p style={{ marginBottom: "1rem" }}>
        Thank you for your interest in participating. In this study, you'll have
        several conversations with an AI assistant over the next couple of weeks.
      </p>
      <p style={{ marginBottom: "1rem" }}>
        Each session takes about 5-10 minutes. You'll chat with the AI about a
        topic of your choice, then answer a few short questions.
      </p>
      <p style={{ marginBottom: "2rem" }}>
        Before we begin, we'll need you to review and agree to the study consent
        form.
      </p>
      <button
        onClick={() => navigate(`/${token}/consent`)}
        style={{
          padding: "0.75rem 2rem",
          backgroundColor: "var(--color-primary)",
          color: "white",
          border: "none",
          borderRadius: "var(--radius)",
          fontSize: "1rem",
        }}
      >
        {participant.consent_given_at ? "Continue to Study" : "Review Consent Form"}
      </button>
    </div>
  );
}
