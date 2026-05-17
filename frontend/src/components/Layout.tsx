import type { ReactNode } from "react";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="mx-auto max-w-3xl min-h-screen px-4 py-8">
      {children}
    </div>
  );
}
