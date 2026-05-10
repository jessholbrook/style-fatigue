import { useState } from "react";
import type { SurveyQuestion } from "../types";
import LikertScale from "./LikertScale";

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
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
      {questions.map((q) => (
        <div key={q.id}>
          <label style={{ display: "block", marginBottom: "0.75rem", fontWeight: 500 }}>
            {q.text}
            {q.required === false && (
              <span style={{ color: "var(--color-text-secondary)", fontWeight: "normal" }}>
                {" "}(optional)
              </span>
            )}
          </label>

          {q.type === "likert" && (
            <LikertScale
              scale={q.scale ?? 7}
              value={responses[q.id] as number | null ?? null}
              onChange={(v) => handleChange(q.id, v)}
              anchors={q.anchors}
            />
          )}

          {q.type === "free_text" && (
            <textarea
              value={q.id === "open_feedback" ? freeText : (responses[q.id] as string ?? "")}
              onChange={(e) => {
                if (q.id === "open_feedback") {
                  setFreeText(e.target.value);
                } else {
                  handleChange(q.id, e.target.value);
                }
              }}
              rows={3}
              style={{
                width: "100%",
                padding: "0.75rem",
                border: "1px solid var(--color-border)",
                borderRadius: "var(--radius)",
                resize: "vertical",
              }}
            />
          )}
        </div>
      ))}

      <button
        type="submit"
        style={{
          padding: "0.75rem 2rem",
          backgroundColor: "var(--color-primary)",
          color: "white",
          border: "none",
          borderRadius: "var(--radius)",
          alignSelf: "flex-end",
        }}
      >
        Submit
      </button>
    </form>
  );
}
