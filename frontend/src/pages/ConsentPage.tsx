import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useParticipant } from "../hooks/useParticipant";
import { recordConsent } from "../api/client";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

export default function ConsentPage() {
  const { participant, token, loading, error } = useParticipant();
  const navigate = useNavigate();
  const [agreed, setAgreed] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (participant?.consent_given_at) {
      navigate(`/${token}/chat`);
    }
  }, [participant?.consent_given_at, token, navigate]);

  if (loading) return <p className="text-muted-foreground">Loading...</p>;
  if (error || !participant)
    return <p className="text-muted-foreground">Invalid or expired study link.</p>;

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
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">Informed Consent</h1>

      <Card>
        <CardContent className="p-6 max-h-[400px] overflow-y-auto space-y-4">
          <div>
            <h3 className="font-semibold mb-1">Study Purpose</h3>
            <p className="text-sm text-muted-foreground">
              This research investigates how people interact with AI assistants over multiple
              sessions. A full description of the study's specific research questions will be
              provided at the end of your participation — some details are withheld now
              because knowing them in advance could influence your responses.
            </p>
          </div>

          <div>
            <h3 className="font-semibold mb-1">What You'll Do</h3>
            <p className="text-sm text-muted-foreground">
              You'll complete several short sessions over approximately two weeks. Each
              session involves a brief conversation with an AI assistant followed by a short
              questionnaire. Sessions take about 5-10 minutes each.
            </p>
          </div>

          <div>
            <h3 className="font-semibold mb-1">Data Collection</h3>
            <p className="text-sm text-muted-foreground">
              We record your conversations, questionnaire responses, and interaction timing.
              No personally identifying information is collected. Your participation is
              identified only by a random token in your study link.
            </p>
          </div>

          <div>
            <h3 className="font-semibold mb-1">Risks & Benefits</h3>
            <p className="text-sm text-muted-foreground">
              There are no known risks beyond those of normal computer use. You may withdraw
              at any time without penalty, and you may request that your data be deleted.
            </p>
          </div>
        </CardContent>
      </Card>

      <div className="flex items-center gap-2">
        <Checkbox
          id="consent"
          checked={agreed}
          onCheckedChange={(checked) => setAgreed(checked === true)}
        />
        <Label htmlFor="consent">I have read and agree to participate in this study</Label>
      </div>

      <Button size="lg" onClick={handleConsent} disabled={!agreed || submitting}>
        {submitting ? "Submitting..." : "I Agree — Begin Study"}
      </Button>
    </div>
  );
}
