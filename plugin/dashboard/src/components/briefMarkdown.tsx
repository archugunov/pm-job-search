import { Text } from "@mantine/core";
import type { Components } from "react-markdown";

// Shared ReactMarkdown component overrides for daily-brief / insights rendering.
// Maps heading and inline elements to compact Mantine Text so the surface
// doesn't blow up with default browser heading sizes.
export const briefMdComponents: Components = {
  // Hide H1 — the surrounding Paper already shows the brief's title.
  h1: () => null,
  h2: ({ children }) => <Text fz="xs" fw={700} mt="md" tt="uppercase" c="dimmed">{children}</Text>,
  h3: ({ children }) => <Text fz="sm" fw={600} mt="sm">{children}</Text>,
  p: ({ children }) => <Text size="sm" my={4}>{children}</Text>,
  ul: ({ children }) => <ul style={{ margin: "4px 0", paddingLeft: 18 }}>{children}</ul>,
  ol: ({ children }) => <ol style={{ margin: "4px 0", paddingLeft: 18 }}>{children}</ol>,
  li: ({ children }) => <li><Text size="sm" component="span">{children}</Text></li>,
  strong: ({ children }) => <Text component="span" fw={700}>{children}</Text>,
  em: ({ children }) => <Text component="span" fs="italic">{children}</Text>,
  code: ({ children }) => (
    <Text component="code" fz="xs" style={{ background: "rgba(255,255,255,0.06)", padding: "1px 4px", borderRadius: 3 }}>
      {children}
    </Text>
  ),
};

// Extract a single H2-bounded section from markdown, by heading regex.
// Returns the section body (lines between the matching ## heading and the next ## heading or EOF).
export function extractSection(markdown: string, headingPattern: RegExp): string | null {
  if (!markdown) return null;
  const lines = markdown.split("\n");
  let inSection = false;
  const captured: string[] = [];
  for (const line of lines) {
    if (line.startsWith("## ")) {
      if (inSection) break; // next H2 starts — stop
      if (headingPattern.test(line)) {
        inSection = true;
        continue;
      }
    }
    if (inSection) captured.push(line);
  }
  const body = captured.join("\n").trim();
  return body.length > 0 ? body : null;
}
