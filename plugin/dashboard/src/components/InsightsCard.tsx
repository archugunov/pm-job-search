import { Paper, Stack, Text } from "@mantine/core";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { briefMdComponents } from "./briefMarkdown";

interface Props {
  markdown: string;
  title?: string;
}

export function InsightsCard({ markdown, title = "Pipeline health" }: Props) {
  return (
    <Paper p="md" radius="lg" bg="dark.8">
      <Stack gap="xs">
        <Text fz="xs" c="dimmed" tt="uppercase" fw={600}>{title}</Text>
        <ReactMarkdown remarkPlugins={[remarkGfm]} components={briefMdComponents}>
          {markdown}
        </ReactMarkdown>
      </Stack>
    </Paper>
  );
}
