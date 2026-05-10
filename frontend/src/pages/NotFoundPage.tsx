export default function NotFoundPage() {
  return (
    <div style={{ textAlign: "center", paddingTop: "3rem" }}>
      <h1 style={{ marginBottom: "1rem" }}>Page Not Found</h1>
      <p style={{ color: "var(--color-text-secondary)" }}>
        This study link is invalid or has expired.
        Please check the link you received and try again.
      </p>
    </div>
  );
}
