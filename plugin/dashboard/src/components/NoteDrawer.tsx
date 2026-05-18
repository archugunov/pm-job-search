import {
  ActionIcon,
  Alert,
  Button,
  Divider,
  Drawer,
  Group,
  Loader,
  Popover,
  Stack,
  Text,
  Textarea,
  Tooltip,
} from "@mantine/core";
import { useHover } from "@mantine/hooks";
import { IconPencil, IconTrash } from "@tabler/icons-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { ApiError, deleteNote, editNote, fetchNotes, postNote } from "../api";

type Flash =
  | { kind: "info"; text: string }
  | { kind: "error"; text: string };

function explainError(action: string, error: unknown): Flash {
  if (error instanceof ApiError && error.status === 409) {
    // The note moved or changed under us (another tab, /today, manual edit).
    return {
      kind: "info",
      text: "This note changed in another window — refreshed.",
    };
  }
  const detail = error instanceof Error ? error.message : String(error);
  return { kind: "error", text: `Couldn't ${action}: ${detail}` };
}

interface Props {
  opened: boolean;
  onClose: () => void;
  folderPath: string;
  company: string;
  position: string;
}

interface Entry {
  fileIndex: number;
  heading: string;
  body: string;
}

function parseEntries(markdown: string): Entry[] {
  if (!markdown.trim()) return [];
  const entries: Entry[] = [];
  let current: { heading: string; body: string } | null = null;
  for (const line of markdown.split("\n")) {
    const m = line.match(/^##\s+(.+?)\s*$/);
    if (m) {
      if (current) {
        entries.push({
          fileIndex: entries.length,
          heading: current.heading,
          body: current.body.trim(),
        });
      }
      current = { heading: m[1], body: "" };
    } else if (current) {
      current.body += line + "\n";
    }
  }
  if (current) {
    entries.push({
      fileIndex: entries.length,
      heading: current.heading,
      body: current.body.trim(),
    });
  }
  return entries;
}

export function NoteDrawer({ opened, onClose, folderPath, company, position }: Props) {
  const [note, setNote] = useState("");
  const [saving, setSaving] = useState(false);
  const [existing, setExisting] = useState<string>("");
  const [loadFailed, setLoadFailed] = useState(false);
  const [loadingExisting, setLoadingExisting] = useState(false);
  const [flash, setFlash] = useState<Flash | null>(null);

  const entries = useMemo(() => parseEntries(existing).slice().reverse(), [existing]);

  // Auto-dismiss flash messages after 4s so the drawer doesn't accumulate noise.
  useEffect(() => {
    if (!flash) return;
    const t = setTimeout(() => setFlash(null), 4000);
    return () => clearTimeout(t);
  }, [flash]);

  // Reset transient state every time the drawer opens against a different position.
  useEffect(() => {
    if (!opened) {
      setFlash(null);
      setLoadFailed(false);
    }
  }, [opened]);

  const refresh = useCallback(async () => {
    if (!folderPath) return;
    setLoadingExisting(true);
    try {
      const markdown = await fetchNotes(folderPath);
      setExisting(markdown);
      setLoadFailed(false);
    } catch {
      setExisting("");
      setLoadFailed(true);
    } finally {
      setLoadingExisting(false);
    }
  }, [folderPath]);

  useEffect(() => {
    if (opened) void refresh();
  }, [opened, refresh]);

  const handleRowError = useCallback(
    async (action: string, error: unknown) => {
      const f = explainError(action, error);
      setFlash(f);
      // 409 means the data shifted under us — pull fresh state so the user
      // sees what's really there rather than staring at a stale entry.
      if (f.kind === "info") await refresh();
    },
    [refresh],
  );

  const submit = async () => {
    if (!note.trim()) return;
    setSaving(true);
    try {
      await postNote(folderPath, note);
      setNote("");
      await refresh();
    } catch (e) {
      setFlash(explainError("add the note", e));
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
      styles={{ title: { fontWeight: 600 } }}
    >
      <Stack gap="lg">
        {flash && (
          <Alert
            variant="light"
            color={flash.kind === "error" ? "red" : "blue"}
            radius="md"
            withCloseButton
            onClose={() => setFlash(null)}
          >
            {flash.text}
          </Alert>
        )}

        {loadFailed && (
          <Alert variant="light" color="yellow" radius="md">
            Couldn't load notes for this position — showing an empty list.
            Check that the dashboard server is running and try opening this note again.
          </Alert>
        )}

        <Stack gap="xs">
          <Textarea
            autosize
            minRows={3}
            radius="md"
            placeholder="What happened?"
            value={note}
            onChange={(e) => setNote(e.currentTarget.value)}
            onKeyDown={(e) => {
              if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
                e.preventDefault();
                void submit();
              }
            }}
          />
          <Button
            fullWidth
            size="sm"
            radius="md"
            loading={saving}
            onClick={submit}
            disabled={!note.trim()}
          >
            Add note
          </Button>
        </Stack>

        <Divider />

        {loadingExisting && <Loader size="sm" />}
        {!loadingExisting && entries.length === 0 && (
          <Text size="sm" c="dimmed">No notes yet.</Text>
        )}
        {!loadingExisting && entries.map((entry, i) => (
          <EntryRow
            key={`${entry.fileIndex}-${entry.heading}`}
            folderPath={folderPath}
            entry={entry}
            onChange={refresh}
            onError={handleRowError}
            isLast={i === entries.length - 1}
          />
        ))}
      </Stack>
    </Drawer>
  );
}

interface EntryRowProps {
  folderPath: string;
  entry: Entry;
  onChange: () => Promise<void>;
  onError: (action: string, error: unknown) => Promise<void>;
  isLast: boolean;
}

function EntryRow({ folderPath, entry, onChange, onError, isLast }: EntryRowProps) {
  const [mode, setMode] = useState<"view" | "edit">("view");
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [draft, setDraft] = useState(entry.body);
  const [busy, setBusy] = useState(false);
  const { hovered, ref } = useHover();
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    setDraft(entry.body);
  }, [entry.body]);

  useEffect(() => {
    if (mode === "edit") {
      // Focus + place cursor at end so the user can keep typing.
      const ta = textareaRef.current;
      if (ta) {
        ta.focus();
        ta.setSelectionRange(ta.value.length, ta.value.length);
      }
    }
  }, [mode]);

  const cancel = useCallback(() => {
    setDraft(entry.body);
    setMode("view");
  }, [entry.body]);

  const saveEdit = useCallback(async () => {
    const trimmed = draft.trim();
    if (!trimmed || trimmed === entry.body.trim()) {
      cancel();
      return;
    }
    setBusy(true);
    try {
      await editNote(folderPath, entry.fileIndex, entry.heading, draft);
      await onChange();
      setMode("view");
    } catch (e) {
      // Drop out of edit mode so the user sees the refreshed state (NoteDrawer
      // pulls fresh notes on 409). Keeping them in the textarea over stale
      // data would just invite a second failure.
      setMode("view");
      await onError("save the note", e);
    } finally {
      setBusy(false);
    }
  }, [cancel, draft, entry.body, entry.fileIndex, entry.heading, folderPath, onChange, onError]);

  const doDelete = async () => {
    setBusy(true);
    try {
      await deleteNote(folderPath, entry.fileIndex, entry.heading);
      setDeleteOpen(false);
      await onChange();
    } catch (e) {
      setDeleteOpen(false);
      await onError("delete the note", e);
    } finally {
      setBusy(false);
    }
  };

  // Actions are visible when the row is hovered, when editing, or when the
  // delete popover is open — so they don't vanish mid-interaction.
  const actionsVisible = hovered || mode === "edit" || deleteOpen;

  return (
    <div
      ref={ref}
      style={{
        paddingBottom: isLast ? 0 : 16,
        borderBottom: isLast ? undefined : "1px solid var(--mantine-color-dark-6)",
      }}
    >
    <Stack gap={6}>
      <Group justify="space-between" align="center" wrap="nowrap" mih={22}>
        <Text size="xs" fw={500} c="dimmed" tt="lowercase" style={{ letterSpacing: 0.2 }}>
          {entry.heading}
        </Text>
        <Group
          gap={2}
          wrap="nowrap"
          style={{
            opacity: actionsVisible ? 1 : 0,
            transition: "opacity 120ms ease",
          }}
        >
          {mode === "view" && (
            <Tooltip label="Edit" openDelay={300} withArrow>
              <ActionIcon
                size="sm"
                variant="subtle"
                color="gray"
                radius="md"
                onClick={() => setMode("edit")}
                aria-label="Edit note"
              >
                <IconPencil size={15} stroke={1.6} />
              </ActionIcon>
            </Tooltip>
          )}
          <Popover
            opened={deleteOpen}
            onChange={setDeleteOpen}
            position="bottom-end"
            withArrow
            shadow="md"
            radius="md"
            width={220}
            trapFocus
          >
            <Popover.Target>
              <Tooltip label="Delete" openDelay={300} withArrow disabled={deleteOpen}>
                <ActionIcon
                  size="sm"
                  variant="subtle"
                  color="gray"
                  radius="md"
                  onClick={() => setDeleteOpen((o) => !o)}
                  aria-label="Delete note"
                >
                  <IconTrash size={15} stroke={1.6} />
                </ActionIcon>
              </Tooltip>
            </Popover.Target>
            <Popover.Dropdown>
              <Stack gap="xs">
                <Text size="sm">Delete this note?</Text>
                <Group justify="flex-end" gap="xs">
                  <Button
                    size="xs"
                    variant="subtle"
                    color="gray"
                    onClick={() => setDeleteOpen(false)}
                    disabled={busy}
                  >
                    Cancel
                  </Button>
                  <Button
                    size="xs"
                    color="red"
                    loading={busy}
                    onClick={doDelete}
                  >
                    Delete
                  </Button>
                </Group>
              </Stack>
            </Popover.Dropdown>
          </Popover>
        </Group>
      </Group>

      {mode === "edit" ? (
        <Stack gap={8}>
          <Textarea
            ref={textareaRef}
            autosize
            minRows={2}
            radius="md"
            value={draft}
            onChange={(e) => setDraft(e.currentTarget.value)}
            disabled={busy}
            onKeyDown={(e) => {
              if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
                e.preventDefault();
                void saveEdit();
              } else if (e.key === "Escape") {
                e.preventDefault();
                cancel();
              }
            }}
          />
          <Group justify="space-between" align="center">
            <Text size="xs" c="dimmed">⌘↵ to save · esc to cancel</Text>
            <Group gap="xs">
              <Button
                size="xs"
                variant="subtle"
                color="gray"
                onClick={cancel}
                disabled={busy}
              >
                Cancel
              </Button>
              <Button
                size="xs"
                radius="md"
                loading={busy}
                onClick={saveEdit}
                disabled={!draft.trim()}
              >
                Save
              </Button>
            </Group>
          </Group>
        </Stack>
      ) : (
        <Text size="sm" style={{ whiteSpace: "pre-wrap", lineHeight: 1.55 }}>
          {entry.body}
        </Text>
      )}
    </Stack>
    </div>
  );
}
