import { useState } from "react";
import { startSession, completeSession } from "../api/client";
import type { ExperimentSession } from "../types";

export function useSession(token: string) {
  const [session, setSession] = useState<ExperimentSession | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function begin() {
    setLoading(true);
    setError(null);
    try {
      const s = await startSession(token);
      setSession(s);
      return s;
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to start session");
      return null;
    } finally {
      setLoading(false);
    }
  }

  async function complete() {
    if (!session) return;
    try {
      const s = await completeSession(token, session.id);
      setSession(s);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to complete session");
    }
  }

  return { session, loading, error, begin, complete };
}
