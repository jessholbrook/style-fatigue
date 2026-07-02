export interface Participant {
  id: string;
  token: string;
  created_at: string;
  consent_given_at: string | null;
  is_active: boolean;
  completed_sessions: number;
}

export interface ExperimentSession {
  id: string;
  session_number: number;
  started_at: string;
  completed_at: string | null;
}

export interface SessionStart {
  session: ExperimentSession;
  conversation: Conversation | null;
  resumed: boolean;
}

export interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export interface Conversation {
  id: string;
  intent: string;
  topic: string;
  messages: Message[];
  turn_count: number;
  started_at: string;
  completed_at: string | null;
}

export interface SurveyQuestion {
  id: string;
  type: "likert" | "free_text" | "multiple_choice";
  text: string;
  scale?: number;
  anchors?: [string, string];
  options?: string[];
  required?: boolean;
}

export interface SurveyInstrument {
  survey_type: string;
  questions: SurveyQuestion[];
}

export interface SurveySubmitResult {
  id: string;
  submitted_at: string;
  study_complete: boolean;
}

export interface IntentItem {
  slug: string;
  label: string;
  topics: string[];
}

export interface StudyConfig {
  max_sessions: number;
  turns_per_conversation: { min: number; max: number };
  session_cooldown_hours: number;
}
