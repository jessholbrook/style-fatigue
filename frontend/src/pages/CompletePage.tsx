import { useParticipant } from "../hooks/useParticipant";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function CompletePage() {
  const { participant, loading } = useParticipant();

  if (loading) return <p className="text-muted-foreground">Loading...</p>;

  return (
    <Card className="text-center">
      <CardHeader>
        <CardTitle className="text-3xl">Session Complete</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-muted-foreground">
          Thank you for completing this session!
        </p>
        {participant && participant.session_count < 6 && (
          <p>
            You've completed {participant.session_count} of 6 sessions.
            Please return in a couple of days for your next session using the same link.
          </p>
        )}
        {participant && participant.session_count >= 6 && (
          <p>
            You've completed all sessions. Thank you for your participation in this study!
          </p>
        )}
      </CardContent>
    </Card>
  );
}
