import { Box, Group, Select, Text } from "@mantine/core";
import { useState } from "react";

import { patchStatus } from "../api";
import { STATUSES, statusColor } from "../statusColors";

const STATUS_OPTIONS = STATUSES.map((s) => ({ value: s.key, label: s.label }));

interface Props {
  folderPath: string;
  current: string;
  onChange: () => void;
}

function StatusDot({ status, size = 8 }: { status: string; size?: number }) {
  return (
    <Box
      w={size}
      h={size}
      style={{
        borderRadius: "50%",
        backgroundColor: statusColor(status),
        flexShrink: 0,
      }}
    />
  );
}

export function StatusSelect({ folderPath, current, onChange }: Props) {
  const [saving, setSaving] = useState(false);
  const [value, setValue] = useState(current);

  return (
    <Select
      size="xs"
      radius={9999}
      variant="filled"
      data={STATUS_OPTIONS}
      value={value}
      disabled={saving}
      leftSection={<StatusDot status={value} />}
      leftSectionWidth={22}
      comboboxProps={{ width: "max-content", middlewares: { flip: true, shift: true } }}
      renderOption={({ option, checked }) => (
        <Group gap="xs" align="center" wrap="nowrap">
          <StatusDot status={option.value} />
          <Text size="sm" fw={checked ? 600 : 400} style={{ whiteSpace: "nowrap" }}>
            {option.label}
          </Text>
        </Group>
      )}
      onChange={async (next) => {
        if (!next || next === value) return;
        setSaving(true);
        setValue(next);
        try {
          await patchStatus(folderPath, next);
          onChange();
        } catch (e) {
          setValue(current);
          alert(`Failed to update status: ${e instanceof Error ? e.message : String(e)}`);
        } finally {
          setSaving(false);
        }
      }}
    />
  );
}
