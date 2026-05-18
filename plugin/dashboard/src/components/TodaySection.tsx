import { Alert, Paper, Stack, Text, TypographyStylesProvider } from "@mantine/core";
import { useMemo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { DailyBrief } from "../types";

interface Props {
  brief: DailyBrief | null;
}

export function TodaySection({ brief }: Props) {
  const today = useMemo(() => new Date().toISOString().slice(0, 10), []);
  const isStale = brief !== null && brief.date < today;

  if (brief === null) {
    return (
      <Paper p="md" withBorder>
        <Text c="dimmed">No daily brief yet — run <Text component="code">/today</Text>.</Text>
      </Paper>
    );
  }

  return (
    <Paper p="md" withBorder>
      <Stack gap="sm">
        <Text fz="sm" c="dimmed" tt="uppercase">
          Today — from daily-brief-{brief.date}.md
        </Text>
        {isStale && (
          <Alert color="yellow">
            Last brief from {brief.date} — run <Text component="code">/today</Text> to refresh.
          </Alert>
        )}
        <TypographyStylesProvider>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{brief.markdown}</ReactMarkdown>
        </TypographyStylesProvider>
      </Stack>
    </Paper>
  );
}
