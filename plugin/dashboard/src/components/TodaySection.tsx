import { Alert, Code, Paper, ScrollArea, Stack, Text } from "@mantine/core";
import { useMemo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { DEMO_MODE } from "../config";
import type { DailyBrief } from "../types";
import { briefMdComponents } from "./briefMarkdown";

interface Props {
  brief: DailyBrief | null;
}

export function TodaySection({ brief }: Props) {
  const today = useMemo(() => new Date().toISOString().slice(0, 10), []);
  // In demo mode the snapshot is pinned to a fixed date — the visitor's
  // wall-clock comparison is meaningless, so always treat the brief as fresh.
  const isStale = !DEMO_MODE && brief !== null && brief.date < today;

  if (brief === null) {
    return (
      <Paper p="md" radius="lg" bg="dark.8" h="100%">
        <Stack gap="xs">
          <Text fz="xs" c="dimmed" tt="uppercase" fw={600}>Daily brief</Text>
          <Text size="sm" c="dimmed">
            No daily brief yet — run <Code>/today</Code>.
          </Text>
        </Stack>
      </Paper>
    );
  }

  return (
    <Paper
      p="md"
      radius="lg"
      bg="dark.8"
      h="100%"
      style={{ display: "flex", flexDirection: "column", overflow: "hidden" }}
    >
      <Stack gap="xs" style={{ height: "100%", minHeight: 0 }}>
        <Text fz="xs" c="dimmed" tt="uppercase" fw={600}>Daily brief — {brief.date}</Text>
        {isStale && (
          <Alert color="yellow" variant="light">
            From {brief.date} — run <Code>/today</Code> to refresh.
          </Alert>
        )}
        <ScrollArea
          style={{ flex: 1, minHeight: 0 }}
          type="hover"
          scrollHideDelay={100}
          scrollbarSize={6}
          styles={{
            thumb: { backgroundColor: "rgba(255,255,255,0.12)" },
            scrollbar: { transition: "opacity 150ms ease" },
          }}
        >
          <ReactMarkdown remarkPlugins={[remarkGfm]} components={briefMdComponents}>
            {stripPipelineSection(brief.markdown)}
          </ReactMarkdown>
        </ScrollArea>
      </Stack>
    </Paper>
  );
}

// Dashboard already surfaces pipeline data via ApplicationsTable + PipelineStats,
// so the brief's `## Pipeline state` section is redundant when rendered here.
// Chat output (the raw .md file) is unaffected.
function stripPipelineSection(md: string): string {
  const lines = md.split("\n");
  const out: string[] = [];
  let skipping = false;
  for (const line of lines) {
    if (/^##\s+Pipeline state\s*$/i.test(line)) {
      skipping = true;
      continue;
    }
    if (skipping && /^##\s/.test(line)) skipping = false;
    if (!skipping) out.push(line);
  }
  return out.join("\n");
}
