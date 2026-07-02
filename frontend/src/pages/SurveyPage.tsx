import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useParticipant } from "../hooks/useParticipant";
import { getSurveyInstrument, submitSurvey, logEvent } from "../api/client";
import { SESSION_STORAGE_KEY } from "../hooks/useSession";
import type { SurveyQuestion } from "../types";
import SurveyForm from "../components/SurveyForm";

export default function SurveyPage() {
  const { token } = useParticipant();
  const navigate = useNavigate();
  const [surveyType, setSurveyType] = useState<"post_conversation" | "exit_survey">(
    "post_conversation"
  );
  const [questions, setQuestions] = useState<SurveyQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const sessionId = sessionStorage.getItem(SESSION_STORAGE_KEY);

  useEffect(() => {
    setLoading(true);
    getSurveyInstrument(surveyType)
      .then((instrument) => {
        setQuestions(instrument.questions);
        if (token && sessionId) {
          logEvent(token, "survey_opened", { survey_type: surveyType }, sessionId);
        }
      })
      .catch(() => setError("Could not load the survey. Please refresh the page."))
      .finally(() => setLoading(false));
  }, [surveyType, token, sessionId]);

  if (!sessionId) {
    return (
      <p className="text-muted-foreground">
        No active session found.{" "}
        <Link to={`/${token}`} className="text-primary underline">
          Return to the study home
        </Link>{" "}
        to continue.
      </p>
    );
  }

  async function handleSubmit(responses: Record<string, unknown>, freeText?: string) {
    setSubmitting(true);
    setError(null);
    try {
      const result = await submitSurvey(token, sessionId!, surveyType, responses, freeText);
      if (surveyType === "post_conversation" && result.study_complete) {
        // Final session: funnel debrief before the thank-you page
        setSurveyType("exit_survey");
        window.scrollTo(0, 0);
      } else {
        sessionStorage.removeItem(SESSION_STORAGE_KEY);
        navigate(`/${token}/complete`);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Submission failed. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <p className="text-muted-foreground">Loading survey...</p>;

  return (
    <div>
      <h1 className="text-3xl font-semibold mb-2">
        {surveyType === "post_conversation" ? "Quick Questions" : "Final Survey"}
      </h1>
      <p className="text-muted-foreground mb-8">
        {surveyType === "post_conversation"
          ? "Please answer a few questions about the conversation you just had."
          : "You've finished all your sessions! A few final questions about your overall experience."}
      </p>
      {error && (
        <p className="text-destructive mb-4" role="alert">
          {error}
        </p>
      )}
      <SurveyForm
        key={surveyType}
        questions={questions}
        onSubmit={handleSubmit}
        submitting={submitting}
      />
    </div>
  );
}
