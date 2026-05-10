export interface Participant {
  id: string;
  token: string;
  condition: string | null;
  created_at: string;
  consent_given_at: string | null;
  is_active: boolean;
  session_count: number;
}

export interface ExperimentSession {
  id: string;
  session_number: number;
  style_profile: string;
  started_at: string;
  completed_at: string | null;
  is_shift_session: boolean;
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

export interface IntentOption {
  slug: string;
  label: string;
  topics: TopicOption[];
}

export interface TopicOption {
  slug: string;
  label: string;
}
