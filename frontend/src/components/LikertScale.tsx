interface Props {
  scale: number;
  value: number | null;
  onChange: (value: number) => void;
  anchors?: [string, string];
}

export default function LikertScale({ scale, value, onChange, anchors }: Props) {
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", gap: "0.25rem" }}>
        {Array.from({ length: scale }, (_, i) => i + 1).map((n) => (
          <button
            key={n}
            onClick={() => onChange(n)}
            style={{
              width: "2.5rem",
              height: "2.5rem",
              borderRadius: "50%",
              border: value === n ? "2px solid var(--color-primary)" : "1px solid var(--color-border)",
              backgroundColor: value === n ? "var(--color-primary)" : "var(--color-surface)",
              color: value === n ? "white" : "var(--color-text)",
              fontWeight: value === n ? "bold" : "normal",
            }}
          >
            {n}
          </button>
        ))}
      </div>
      {anchors && (
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginTop: "0.25rem",
            fontSize: "0.75rem",
            color: "var(--color-text-secondary)",
          }}
        >
          <span>{anchors[0]}</span>
          <span>{anchors[1]}</span>
        </div>
      )}
    </div>
  );
}
