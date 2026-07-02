import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useParticipant } from "../hooks/useParticipant";
import { logEvent } from "../api/client";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function LandingPage() {
  const { participant, token, loading, error } = useParticipant();
  const navigate = useNavigate();

  useEffect(() => {
    if (participant) {
      logEvent(token, "page_view", { page: "landing" });
    }
  }, [participant, token]);

  if (loading) return <p className="text-muted-foreground">Loading...</p>;
  if (error || !participant)
    return <p className="text-muted-foreground">Invalid or expired study link.</p>;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-3xl">Welcome to the Study</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p>
          Thank you for your interest in participating. In this study, you'll have several
          conversations with an AI assistant over the next couple of weeks.
        </p>
        <p>
          Each session takes about 5-10 minutes. You'll chat with the AI about a topic of
          your choice, then answer a few short questions.
        </p>
        <p>
          Before we begin, we'll need you to review and agree to the study consent form.
        </p>
        <Button size="lg" onClick={() => navigate(`/${token}/consent`)}>
          {participant.consent_given_at ? "Continue to Study" : "Review Consent Form"}
        </Button>
      </CardContent>
    </Card>
  );
}
