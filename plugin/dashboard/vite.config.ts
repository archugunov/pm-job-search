import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Node's `process` global isn't typed in this config (no @types/node), but
// it's available at runtime — Vite executes this file under Node.
declare const process: { env: Record<string, string | undefined> };

// `base` is overridable for the GitHub Pages demo build:
// VITE_BASE=/pm-job-search/ npm run build
const base = process.env.VITE_BASE ?? "/";

export default defineConfig({
  base,
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://localhost:7890",
    },
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
    target: "es2020",
  },
});
