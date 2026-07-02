import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import SurveyForm from "@/components/SurveyForm";
import LikertScale from "@/components/LikertScale";
import type { SurveyQuestion } from "@/types";

describe("LikertScale", () => {
  it("reports the clicked value", () => {
    const onChange = vi.fn();
    render(<LikertScale scale={7} value={null} onChange={onChange} />);
    fireEvent.click(screen.getByRole("button", { name: "5" }));
    expect(onChange).toHaveBeenCalledWith(5);
  });
});

describe("SurveyForm", () => {
  const questions: SurveyQuestion[] = [
    { id: "q1", type: "likert", scale: 7, text: "Rate this", required: true },
    {
      id: "q2",
      type: "multiple_choice",
      text: "Pick one",
      options: ["Option A", "Option B"],
      required: true,
    },
  ];

  it("blocks submission with a visible error when required questions are unanswered", () => {
    const onSubmit = vi.fn();
    render(<SurveyForm questions={questions} onSubmit={onSubmit} />);
    fireEvent.click(screen.getByRole("button", { name: "Submit" }));
    expect(onSubmit).not.toHaveBeenCalled();
    expect(screen.getByRole("alert")).toBeInTheDocument();
  });

  it("submits when all required questions are answered", () => {
    const onSubmit = vi.fn();
    render(<SurveyForm questions={questions} onSubmit={onSubmit} />);
    fireEvent.click(screen.getByRole("button", { name: "4" }));
    fireEvent.click(screen.getByLabelText("Option A"));
    fireEvent.click(screen.getByRole("button", { name: "Submit" }));
    expect(onSubmit).toHaveBeenCalledWith({ q1: 4, q2: "Option A" }, undefined);
  });
});
