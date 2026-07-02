import { useState } from "react";
import { startSession } from "../api/client";
import type { SessionStart } from "../types";

export const SESSION_STORAGE_KEY = "current_session_id";

export function useSession(token: string) {
  const [sessionStart, setSessionStart] = useState<SessionStart | null>(null);
  const [loading, setLoading] = useState(false);

  async function begin(): Promise<SessionStart> {
    setLoading(true);
    try {
      const start = await startSession(token);
      setSessionStart(start);
      sessionStorage.setItem(SESSION_STORAGE_KEY, start.session.id);
      return start;
    } finally {
      setLoading(false);
    }
  }

  return { sessionStart, session: sessionStart?.session ?? null, loading, begin };
}
