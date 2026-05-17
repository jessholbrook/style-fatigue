import { cn } from "@/lib/utils";

interface Props {
  scale: number;
  value: number | null;
  onChange: (value: number) => void;
  anchors?: [string, string];
}

export default function LikertScale({ scale, value, onChange, anchors }: Props) {
  return (
    <div>
      <div className="flex justify-between gap-1">
        {Array.from({ length: scale }, (_, i) => i + 1).map((n) => (
          <button
            key={n}
            type="button"
            onClick={() => onChange(n)}
            className={cn(
              "w-10 h-10 rounded-full border text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
              value === n
                ? "border-primary bg-primary text-primary-foreground"
                : "border-input bg-background text-foreground hover:bg-accent"
            )}
          >
            {n}
          </button>
        ))}
      </div>
      {anchors && (
        <div className="flex justify-between mt-1 text-xs text-muted-foreground">
          <span>{anchors[0]}</span>
          <span>{anchors[1]}</span>
        </div>
      )}
    </div>
  );
}
