import { Paper, Text } from "@mantine/core";
import type { Position } from "../types";

interface Props {
  companies: Position[];
  userdataRoot: string;
  onChange: () => void;
}

export function ApplicationsTable({ companies, userdataRoot: _userdataRoot, onChange: _onChange }: Props) {
  return (
    <Paper p="md" withBorder>
      <Text>ApplicationsTable placeholder — {companies.length} positions</Text>
    </Paper>
  );
}
