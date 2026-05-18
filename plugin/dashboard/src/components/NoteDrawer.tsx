import { Button, Divider, Drawer, Loader, Stack, Text, Textarea, TypographyStylesProvider } from "@mantine/core";
import { useCallback, useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { fetchNotes, postNote } from "../api";

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
  const [existing, setExisting] = useState<string | null>(null);
  const [loadingExisting, setLoadingExisting] = useState(false);

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
      title={position ? `Notes — ${company} · ${position}` : `Notes — ${company}`}
      position="right"
      size="md"
    >
      <Stack>
        {loadingExisting && <Loader size="sm" />}
        {!loadingExisting && existing && existing.trim().length > 0 && (
          <TypographyStylesProvider>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{existing}</ReactMarkdown>
          </TypographyStylesProvider>
        )}
        {!loadingExisting && (!existing || existing.trim().length === 0) && (
          <Text size="sm" c="dimmed">No notes yet.</Text>
        )}
        <Divider label="Add note" labelPosition="left" />
        <Textarea
          autosize
          minRows={4}
          placeholder="What happened?"
          value={note}
          onChange={(e) => setNote(e.currentTarget.value)}
        />
        <Button loading={saving} onClick={submit} disabled={!note.trim()}>Save note</Button>
      </Stack>
    </Drawer>
  );
}
