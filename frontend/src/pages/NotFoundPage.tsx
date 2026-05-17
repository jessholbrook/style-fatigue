import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function NotFoundPage() {
  return (
    <Card className="text-center">
      <CardHeader>
        <CardTitle className="text-3xl">Page Not Found</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-muted-foreground">
          This study link is invalid or has expired.
          Please check the link you received and try again.
        </p>
      </CardContent>
    </Card>
  );
}
