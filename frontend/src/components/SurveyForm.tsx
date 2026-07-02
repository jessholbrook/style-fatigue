import { useState } from "react";
import type { SurveyQuestion } from "../types";
import LikertScale from "./LikertScale";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

interface Props {
  questions: SurveyQuestion[];
  onSubmit: (responses: Record<string, unknown>, freeText?: string) => void;
  submitting?: boolean;
}

export default function SurveyForm({ questions, onSubmit, submitting = false }: Props) {
  const [responses, setResponses] = useState<Record<string, unknown>>({});
  const [freeText, setFreeText] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  function handleChange(questionId: string, value: unknown) {
    setResponses((prev) => ({ ...prev, [questionId]: value }));
    setValidationError(null);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const missing = questions.filter(
      (q) => q.required !== false && q.type !== "free_text" && responses[q.id] == null
    );
    if (missing.length > 0) {
      setValidationError(
        missing.length === 1
          ? "Please answer the highlighted question before submitting."
          : `Please answer all ${missing.length} remaining questions before submitting.`
      );
      return;
    }

    onSubmit(responses, freeText || undefined);
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-8">
      {questions.map((q) => (
        <div key={q.id}>
          <Label className="block mb-3 text-base font-medium">
            {q.text}
            {q.required === false && (
              <span className="text-muted-foreground font-normal"> (optional)</span>
            )}
          </Label>

          {q.type === "likert" && (
            <LikertScale
              scale={q.scale ?? 7}
              value={(responses[q.id] as number | null) ?? null}
              onChange={(v) => handleChange(q.id, v)}
              anchors={q.anchors}
            />
          )}

          {q.type === "multiple_choice" && (
            <RadioGroup
              value={(responses[q.id] as string) ?? ""}
              onValueChange={(v) => handleChange(q.id, v)}
            >
              {(q.options ?? []).map((option) => (
                <div key={option} className="flex items-center gap-2">
                  <RadioGroupItem value={option} id={`${q.id}-${option}`} />
                  <Label htmlFor={`${q.id}-${option}`} className="font-normal cursor-pointer">
                    {option}
                  </Label>
                </div>
              ))}
            </RadioGroup>
          )}

          {q.type === "free_text" && (
            <Textarea
              value={q.id === "open_feedback" ? freeText : ((responses[q.id] as string) ?? "")}
              onChange={(e) => {
                if (q.id === "open_feedback") {
                  setFreeText(e.target.value);
                } else {
                  handleChange(q.id, e.target.value);
                }
              }}
              rows={3}
            />
          )}
        </div>
      ))}

      {validationError && (
        <p className="text-sm text-destructive" role="alert">
          {validationError}
        </p>
      )}

      <Button type="submit" className="self-end" disabled={submitting}>
        {submitting ? "Submitting..." : "Submit"}
      </Button>
    </form>
  );
}
