import { Button, Divider, Drawer, Loader, Stack, Text, Textarea } from "@mantine/core";
import { useCallback, useEffect, useMemo, useState } from "react";

import { fetchNotes, postNote } from "../api";

interface Props {
  opened: boolean;
  onClose: () => void;
  folderPath: string;
  company: string;
  position: string;
}

interface Entry {
  date: string;
  body: string;
}

function parseEntries(markdown: string): Entry[] {
  if (!markdown.trim()) return [];
  const entries: Entry[] = [];
  let current: Entry | null = null;
  for (const line of markdown.split("\n")) {
    const m = line.match(/^##\s+(.+?)\s*$/);
    if (m) {
      if (current) entries.push({ ...current, body: current.body.trim() });
      current = { date: m[1], body: "" };
    } else if (current) {
      current.body += line + "\n";
    }
  }
  if (current) entries.push({ ...current, body: current.body.trim() });
  return entries;
}

export function NoteDrawer({ opened, onClose, folderPath, company, position }: Props) {
  const [note, setNote] = useState("");
  const [saving, setSaving] = useState(false);
  const [existing, setExisting] = useState<string>("");
  const [loadingExisting, setLoadingExisting] = useState(false);

  const entries = useMemo(() => parseEntries(existing).reverse(), [existing]);

  const refresh = useCallback(async () => {
    if (!folderPath) return;
    setLoadingExisting(true);
    try {
      const markdown = await fetchNotes(folderPath);
      setExisting(markdown);
    } catch {
      setExisting("");
    } finally {
      setLoadingExisting(false);
    }
  }, [folderPath]);

  useEffect(() => {
    if (opened) void refresh();
  }, [opened, refresh]);

  const submit = async () => {
    if (!note.trim()) return;
    setSaving(true);
    try {
      await postNote(folderPath, note);
      setNote("");
      await refresh();
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
      title={position ? `${company} · ${position}` : company}
      position="right"
      size="md"
    >
      <Stack gap="md">
        <Textarea
          autosize
          minRows={3}
          placeholder="What happened?"
          value={note}
          onChange={(e) => setNote(e.currentTarget.value)}
        />
        <Button loading={saving} onClick={submit} disabled={!note.trim()}>Save note</Button>

        <Divider />

        {loadingExisting && <Loader size="sm" />}
        {!loadingExisting && entries.length === 0 && (
          <Text size="sm" c="dimmed">No notes yet.</Text>
        )}
        {!loadingExisting && entries.map((e, i) => (
          <Stack key={i} gap={4}>
            <Text size="xs" fw={600} c="dimmed">{e.date}</Text>
            <Text size="sm" style={{ whiteSpace: "pre-wrap" }}>{e.body}</Text>
          </Stack>
        ))}
      </Stack>
    </Drawer>
  );
}
