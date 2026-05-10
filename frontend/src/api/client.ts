import type {
  Participant,
  ExperimentSession,
  Conversation,
  SurveyInstrument,
} from "../types";

const BASE_URL = "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

export function getParticipant(token: string) {
  return request<Participant>(`/participants/${token}`);
}

export function recordConsent(token: string) {
  return request<Participant>(`/participants/${token}/consent`, {
    method: "POST",
    body: JSON.stringify({ agreed: true }),
  });
}

export function startSession(token: string) {
  return request<ExperimentSession>(`/participants/${token}/sessions`, {
    method: "POST",
  });
}

export function listSessions(token: string) {
  return request<ExperimentSession[]>(`/participants/${token}/sessions`);
}

export function completeSession(token: string, sessionId: string) {
  return request<ExperimentSession>(
    `/participants/${token}/sessions/${sessionId}/complete`,
    { method: "POST" }
  );
}

export function startConversation(
  sessionId: string,
  intent: string,
  topic: string
) {
  return request<Conversation>(`/sessions/${sessionId}/conversations`, {
    method: "POST",
    body: JSON.stringify({ intent, topic }),
  });
}

export function sendMessage(
  sessionId: string,
  conversationId: string,
  content: string
) {
  return request<Conversation>(
    `/sessions/${sessionId}/conversations/${conversationId}/messages`,
    {
      method: "POST",
      body: JSON.stringify({ content }),
    }
  );
}

export function getSurveyInstrument(surveyType: string) {
  return request<SurveyInstrument>(`/surveys/${surveyType}`);
}

export function submitSurvey(
  sessionId: string,
  surveyType: string,
  responses: Record<string, unknown>,
  freeText?: string
) {
  return request(`/sessions/${sessionId}/surveys`, {
    method: "POST",
    body: JSON.stringify({
      survey_type: surveyType,
      responses,
      free_text: freeText,
    }),
  });
}

export function getIntents() {
  return request<{ intents: Array<{ slug: string; label: string; topics: string[] }> }>(
    `/intents`
  );
}
