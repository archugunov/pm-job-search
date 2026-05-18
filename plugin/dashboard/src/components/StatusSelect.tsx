import { Select } from "@mantine/core";
import { useState } from "react";

import { patchStatus } from "../api";

const STATUS_OPTIONS = [
  "discovered",
  "applied",
  "interviewing",
  "offer-received",
  "rejected",
  "withdrew",
  "paused",
];

interface Props {
  folderPath: string;
  current: string;
  onChange: () => void;
}

export function StatusSelect({ folderPath, current, onChange }: Props) {
  const [saving, setSaving] = useState(false);
  const [value, setValue] = useState(current);

  return (
    <Select
      size="xs"
      data={STATUS_OPTIONS}
      value={value}
      disabled={saving}
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
