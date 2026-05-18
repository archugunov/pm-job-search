import { Paper, Text } from "@mantine/core";
import type { Position, Strategy } from "../types";

interface Props {
  companies: Position[];
  strategy: Strategy;
}

export function PipelineStats({ companies, strategy: _strategy }: Props) {
  return (
    <Paper p="md" withBorder>
      <Text>PipelineStats placeholder — {companies.length} companies</Text>
    </Paper>
  );
}
