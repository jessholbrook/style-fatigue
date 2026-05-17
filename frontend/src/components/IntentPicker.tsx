import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

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
      <h2 className="text-2xl font-semibold mb-2">What would you like to do?</h2>
      <p className="text-muted-foreground mb-6">
        Choose a task and topic for this session's conversation.
      </p>
      <div className="flex flex-col gap-4">
        {intents.map((intent) => (
          <Card key={intent.slug}>
            <CardHeader className="pb-3">
              <CardTitle className="text-lg">{intent.label}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {intent.topics.map((topic) => (
                  <Button
                    key={topic}
                    variant="outline"
                    size="sm"
                    onClick={() => onSelect(intent.slug, topic)}
                  >
                    {topic.replace(/_/g, " ")}
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
