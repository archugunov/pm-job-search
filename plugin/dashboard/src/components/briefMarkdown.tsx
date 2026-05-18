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
