import { useState } from "react";
import type { SurveyQuestion } from "../types";
import LikertScale from "./LikertScale";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

interface Props {
  questions: SurveyQuestion[];
  onSubmit: (responses: Record<string, unknown>, freeText?: string) => void;
}

export default function SurveyForm({ questions, onSubmit }: Props) {
  const [responses, setResponses] = useState<Record<string, unknown>>({});
  const [freeText, setFreeText] = useState("");

  function handleChange(questionId: string, value: unknown) {
    setResponses((prev) => ({ ...prev, [questionId]: value }));
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const required = questions.filter((q) => q.required !== false);
    const allAnswered = required.every((q) => responses[q.id] != null);
    if (!allAnswered) return;

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

      <Button type="submit" className="self-end">
        Submit
      </Button>
    </form>
  );
}
