import type {
  Participant,
  SessionStart,
  ExperimentSession,
  Conversation,
  SurveyInstrument,
  SurveySubmitResult,
  IntentItem,
  StudyConfig,
} from "../types";

const BASE_URL = "/api";

export class ApiError extends Error {
  status: number;
  detail: unknown;

  constructor(status: number, detail: unknown) {
    super(typeof detail === "string" ? detail : `HTTP ${status}`);
    this.status = status;
    this.detail = detail;
  }
}

export function detailReason(error: unknown): string | null {
  if (error instanceof ApiError && error.detail && typeof error.detail === "object") {
    return (error.detail as { reason?: string }).reason ?? null;
  }
  return null;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    let detail: unknown = null;
    try {
      detail = (await response.json()).detail;
    } catch {
      // non-JSON error body
    }
    throw new ApiError(response.status, detail);
  }
  if (response.status === 204) {
    return undefined as T;
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
  return request<SessionStart>(`/participants/${token}/sessions`, {
    method: "POST",
  });
}

export function listSessions(token: string) {
  return request<ExperimentSession[]>(`/participants/${token}/sessions`);
}

export function getIntents(token: string) {
  return request<{ intents: IntentItem[] }>(`/participants/${token}/intents`);
}

export function getConfig() {
  return request<StudyConfig>(`/config`);
}

export function startConversation(
  token: string,
  sessionId: string,
  intent: string,
  topic: string
) {
  return request<Conversation>(
    `/participants/${token}/sessions/${sessionId}/conversations`,
    {
      method: "POST",
      body: JSON.stringify({ intent, topic }),
    }
  );
}

export function sendMessage(
  token: string,
  sessionId: string,
  conversationId: string,
  content: string
) {
  return request<Conversation>(
    `/participants/${token}/sessions/${sessionId}/conversations/${conversationId}/messages`,
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
  token: string,
  sessionId: string,
  surveyType: string,
  responses: Record<string, unknown>,
  freeText?: string
) {
  return request<SurveySubmitResult>(
    `/participants/${token}/sessions/${sessionId}/surveys`,
    {
      method: "POST",
      body: JSON.stringify({
        survey_type: surveyType,
        responses,
        free_text: freeText,
      }),
    }
  );
}

/** Fire-and-forget behavioral beacon; never blocks or throws. */
export function logEvent(
  token: string,
  eventType: string,
  payload: Record<string, unknown> = {},
  sessionId?: string
) {
  request(`/participants/${token}/events`, {
    method: "POST",
    body: JSON.stringify({
      event_type: eventType,
      payload,
      session_id: sessionId ?? null,
      client_timestamp: new Date().toISOString(),
    }),
  }).catch(() => {
    // instrumentation must never break the participant experience
  });
}
