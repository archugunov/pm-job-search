import { Alert, Paper, Spoiler, Stack, Text } from "@mantine/core";
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
      <Paper p="md" withBorder>
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
    <Paper p="md" withBorder>
      <Stack gap="xs">
        <Text fz="xs" c="dimmed" tt="uppercase" fw={600}>Daily brief — {brief.date}</Text>
        {isStale && (
          <Alert color="yellow" variant="light">
            From {brief.date} — run <Text component="code">/today</Text> to refresh.
          </Alert>
        )}
        <Spoiler maxHeight={220} showLabel="Show more" hideLabel="Show less">
          <ReactMarkdown remarkPlugins={[remarkGfm]} components={briefMdComponents}>
            {brief.markdown}
          </ReactMarkdown>
        </Spoiler>
      </Stack>
    </Paper>
  );
}
