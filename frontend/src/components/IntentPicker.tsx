interface IntentItem {
  slug: string;
  label: string;
  topics: string[];
}

interface Props {
  intents: IntentItem[];
  onSelect: (intent: string, topic: string) => void;
}

export default function IntentPicker({ intents, onSelect }: Props) {
  return (
    <div>
      <h2 style={{ marginBottom: "1rem" }}>What would you like to do?</h2>
      <p style={{ color: "var(--color-text-secondary)", marginBottom: "1.5rem" }}>
        Choose a task and topic for this session's conversation.
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        {intents.map((intent) => (
          <div
            key={intent.slug}
            style={{
              border: "1px solid var(--color-border)",
              borderRadius: "var(--radius)",
              padding: "1rem",
            }}
          >
            <h3 style={{ marginBottom: "0.5rem" }}>{intent.label}</h3>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
              {intent.topics.map((topic) => (
                <button
                  key={topic}
                  onClick={() => onSelect(intent.slug, topic)}
                  style={{
                    padding: "0.5rem 1rem",
                    backgroundColor: "var(--color-surface)",
                    border: "1px solid var(--color-border)",
                    borderRadius: "var(--radius)",
                    fontSize: "0.875rem",
                  }}
                >
                  {topic.replace(/_/g, " ")}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
