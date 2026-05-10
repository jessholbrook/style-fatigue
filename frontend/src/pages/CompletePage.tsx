import { useParticipant } from "../hooks/useParticipant";

export default function CompletePage() {
  const { participant, loading } = useParticipant();

  if (loading) return <p>Loading...</p>;

  return (
    <div style={{ textAlign: "center", paddingTop: "3rem" }}>
      <h1 style={{ marginBottom: "1rem" }}>Session Complete</h1>
      <p style={{ marginBottom: "1rem", color: "var(--color-text-secondary)" }}>
        Thank you for completing this session!
      </p>
      {participant && participant.session_count < 6 && (
        <p style={{ marginBottom: "2rem" }}>
          You've completed {participant.session_count} of 6 sessions.
          Please return in a couple of days for your next session using the same link.
        </p>
      )}
      {participant && participant.session_count >= 6 && (
        <p style={{ marginBottom: "2rem" }}>
          You've completed all sessions. Thank you for your participation in this study!
        </p>
      )}
    </div>
  );
}
