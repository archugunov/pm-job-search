import { Alert, Button, Modal, Select, Stack, TextInput } from "@mantine/core";
import { useState } from "react";

import { postPosition } from "../api";

const STATUS_OPTIONS = [
  "new",
  "applied",
  "interviewing",
  "offer",
  "rejected",
  "closed",
];

interface Props {
  opened: boolean;
  onClose: () => void;
  onCreated: () => void;
}

export function NewPositionModal({ opened, onClose, onCreated }: Props) {
  const [link, setLink] = useState("");
  const [status, setStatus] = useState<string>("new");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const reset = () => {
    setLink("");
    setStatus("new");
    setError(null);
  };

  const submit = async () => {
    setError(null);
    if (!link.trim()) {
      setError("A link is required.");
      return;
    }
    setSaving(true);
    try {
      await postPosition({ link: link.trim(), status });
      reset();
      onCreated();
      onClose();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create position");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal opened={opened} onClose={onClose} title="New position" centered>
      <Stack>
        <TextInput
          label="Link"
          placeholder="https://company.com/jobs/..."
          value={link}
          onChange={(e) => setLink(e.currentTarget.value)}
          required
          autoFocus
        />
        <Select
          label="Status"
          data={STATUS_OPTIONS}
          value={status}
          onChange={(v) => v && setStatus(v)}
        />
        {error && <Alert color="red">{error}</Alert>}
        <Button loading={saving} onClick={submit}>Create</Button>
      </Stack>
    </Modal>
  );
}
