import { Code, Text } from "@mantine/core";
import type { Components } from "react-markdown";

// Component map for the daily brief surface. The brief sits inside a titled
// Paper, so h2 section headings are kept compact and dimmed.
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
  code: ({ children }) => <Code>{children}</Code>,
};

// Component map for the company drawer (Research / Prep / Debriefs). These
// docs use h2 as the spine of the structure (Company snapshot / Why this fits
// / Open questions etc.), so headings need real presence for scannability.
export const companyDocMdComponents: Components = {
  h1: () => null,
  h2: ({ children }) => (
    <Text fz="sm" fw={700} mt="lg" mb={6}>{children}</Text>
  ),
  h3: ({ children }) => <Text fz="sm" fw={600} mt="md" mb={2}>{children}</Text>,
  p: ({ children }) => <Text size="sm" my={6} style={{ lineHeight: 1.55 }}>{children}</Text>,
  ul: ({ children }) => (
    <ul style={{ margin: "6px 0", paddingLeft: 20 }}>{children}</ul>
  ),
  ol: ({ children }) => (
    <ol style={{ margin: "6px 0", paddingLeft: 20 }}>{children}</ol>
  ),
  li: ({ children }) => (
    <li style={{ marginBottom: 4 }}>
      <Text size="sm" component="span" style={{ lineHeight: 1.55 }}>{children}</Text>
    </li>
  ),
  strong: ({ children }) => <Text component="span" fw={700}>{children}</Text>,
  em: ({ children }) => <Text component="span" fs="italic">{children}</Text>,
  code: ({ children }) => <Code>{children}</Code>,
};
