import { Button, Drawer, Stack, Text, Textarea } from "@mantine/core";
import { useState } from "react";

import { postNote } from "../api";

interface Props {
  opened: boolean;
  onClose: () => void;
  folderPath: string;
  company: string;
  position: string;
}

export function NoteDrawer({ opened, onClose, folderPath, company, position }: Props) {
  const [note, setNote] = useState("");
  const [saving, setSaving] = useState(false);

  const submit = async () => {
    if (!note.trim()) return;
    setSaving(true);
    try {
      await postNote(folderPath, note);
      setNote("");
      onClose();
    } catch (e) {
      alert(`Failed to add note: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setSaving(false);
    }
  };

  return (
    <Drawer
      opened={opened}
      onClose={onClose}
      title={`Note — ${company} · ${position}`}
      position="right"
      size="md"
    >
      <Stack>
        <Text size="sm" c="dimmed">
          Appended to notes.md alongside this position's meta.md with a timestamp.
        </Text>
        <Textarea
          autosize
          minRows={6}
          placeholder="What happened?"
          value={note}
          onChange={(e) => setNote(e.currentTarget.value)}
        />
        <Button loading={saving} onClick={submit}>Save note</Button>
      </Stack>
    </Drawer>
  );
}
