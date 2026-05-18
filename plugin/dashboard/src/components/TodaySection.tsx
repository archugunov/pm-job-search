import { Alert, Paper, ScrollArea, Stack, Text } from "@mantine/core";
import { useMemo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { DailyBrief } from "../types";
import { briefMdComponents } from "./briefMarkdown";

interface Props {
  brief: DailyBrief | null;
}

export function TodaySection({ brief }: Props) {
  const today = useMemo(() => new Date().toISOString().slice(0, 10), []);
  const isStale = brief !== null && brief.date < today;

  if (brief === null) {
    return (
      <Paper p="md" radius="lg" bg="dark.8" h="100%">
        <Stack gap="xs">
          <Text fz="xs" c="dimmed" tt="uppercase" fw={600}>Daily brief</Text>
          <Text size="sm" c="dimmed">
            No daily brief yet — run <Text component="code">/today</Text>.
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
            From {brief.date} — run <Text component="code">/today</Text> to refresh.
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
            {brief.markdown}
          </ReactMarkdown>
        </ScrollArea>
      </Stack>
    </Paper>
  );
}
