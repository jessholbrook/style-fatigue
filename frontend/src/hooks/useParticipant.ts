import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getParticipant } from "../api/client";
import type { Participant } from "../types";

export function useParticipant() {
  const { token } = useParams<{ token: string }>();
  const [participant, setParticipant] = useState<Participant | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    getParticipant(token)
      .then(setParticipant)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [token]);

  return { participant, token: token ?? "", loading, error, refetch: () => {
    if (!token) return;
    getParticipant(token).then(setParticipant);
  }};
}
