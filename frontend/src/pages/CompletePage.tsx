import { useEffect, useState } from "react";
import { useParticipant } from "../hooks/useParticipant";
import { getConfig } from "../api/client";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function CompletePage() {
  const { participant, loading } = useParticipant();
  const [maxSessions, setMaxSessions] = useState(6);

  useEffect(() => {
    getConfig()
      .then((c) => setMaxSessions(c.max_sessions))
      .catch(() => {
        // fall back to the default
      });
  }, []);

  if (loading) return <p className="text-muted-foreground">Loading...</p>;

  const done = participant ? participant.completed_sessions : 0;
  const finished = done >= maxSessions;

  return (
    <Card className="text-center">
      <CardHeader>
        <CardTitle className="text-3xl">
          {finished ? "Study Complete" : "Session Complete"}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-muted-foreground">Thank you for completing this session!</p>
        {!finished && (
          <p>
            You've completed {done} of {maxSessions} sessions. Please return in a couple of
            days for your next session using the same link.
          </p>
        )}
        {finished && (
          <>
            <p>
              You've completed all {maxSessions} sessions. Thank you for your participation!
            </p>
            <div className="text-left text-sm text-muted-foreground border rounded-lg p-4 space-y-2">
              <p className="font-medium text-foreground">About this study</p>
              <p>
                Now that you've finished, we can share the full purpose of this research: we
                are studying how people notice and adapt to changes in an AI assistant's
                communication style over repeated sessions. For some participants, the
                assistant's writing style was deliberately changed partway through the study;
                for others it stayed the same throughout.
              </p>
              <p>
                We didn't describe this in advance because knowing the study was about style
                changes would have affected what you noticed. Your conversations and survey
                answers are stored without any personally identifying information. If you have
                questions or would like your data withdrawn, please contact the research team
                via the platform where you enrolled.
              </p>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
