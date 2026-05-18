import { Paper, Text } from "@mantine/core";
import type { DailyBrief } from "../types";

interface Props {
  brief: DailyBrief | null;
}

export function TodaySection({ brief }: Props) {
  return (
    <Paper p="md" withBorder>
      <Text>TodaySection placeholder — brief {brief ? brief.date : "absent"}</Text>
    </Paper>
  );
}
