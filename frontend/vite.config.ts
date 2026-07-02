import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(dirname, "./src"),
    },
  },
  server: {
    proxy: {
      "/api": {
        // In docker-compose the backend is at http://backend:8000 (set via VITE_API_URL)
        target: process.env.VITE_API_URL ?? "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
  },
});
