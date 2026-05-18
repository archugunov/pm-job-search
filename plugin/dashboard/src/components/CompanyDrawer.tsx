import {
  ActionIcon,
  Alert,
  Badge,
  Button,
  Code,
  Drawer,
  Group,
  Loader,
  Popover,
  Stack,
  Tabs,
  Text,
  Textarea,
  Tooltip,
} from "@mantine/core";
import { useHover } from "@mantine/hooks";
import { IconPencil, IconTrash } from "@tabler/icons-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { Artifacts, DebriefDoc, PrepDoc } from "../api";
import {
  ApiError,
  deleteNote,
  editNote,
  fetchArtifacts,
  fetchNotes,
  postNote,
} from "../api";
import { briefMdComponents } from "./briefMarkdown";

type Flash =
  | { kind: "info"; text: string }
  | { kind: "error"; text: string };

function explainError(action: string, error: unknown): Flash {
  if (error instanceof ApiError && error.status === 409) {
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

type TabKey = "notes" | "research" | "prep" | "debriefs";

export function CompanyDrawer({ opened, onClose, folderPath, company, position }: Props) {
  const [activeTab, setActiveTab] = useState<TabKey>("notes");
  const [flash, setFlash] = useState<Flash | null>(null);

  // Notes state — owned at this level so edit/delete + add can share refresh.
  const [notesMarkdown, setNotesMarkdown] = useState<string>("");
  const [notesLoading, setNotesLoading] = useState(false);
  const [notesLoadFailed, setNotesLoadFailed] = useState(false);

  // Artifacts state — single fetch per drawer open.
  const [artifacts, setArtifacts] = useState<Artifacts | null>(null);
  const [artifactsLoading, setArtifactsLoading] = useState(false);
  const [artifactsLoadFailed, setArtifactsLoadFailed] = useState(false);

  const notesEntries = useMemo(
    () => parseEntries(notesMarkdown).slice().reverse(),
    [notesMarkdown],
  );

  // Auto-dismiss flash after 4s.
  useEffect(() => {
    if (!flash) return;
    const t = setTimeout(() => setFlash(null), 4000);
    return () => clearTimeout(t);
  }, [flash]);

  // Reset everything when the drawer closes.
  useEffect(() => {
    if (!opened) {
      setActiveTab("notes");
      setFlash(null);
      setNotesLoadFailed(false);
      setArtifactsLoadFailed(false);
    }
  }, [opened]);

  const refreshNotes = useCallback(async () => {
    if (!folderPath) return;
    setNotesLoading(true);
    try {
      const md = await fetchNotes(folderPath);
      setNotesMarkdown(md);
      setNotesLoadFailed(false);
    } catch {
      setNotesMarkdown("");
      setNotesLoadFailed(true);
    } finally {
      setNotesLoading(false);
    }
  }, [folderPath]);

  const refreshArtifacts = useCallback(async () => {
    if (!folderPath) return;
    setArtifactsLoading(true);
    try {
      const a = await fetchArtifacts(folderPath);
      setArtifacts(a);
      setArtifactsLoadFailed(false);
    } catch {
      setArtifacts({ research: null, preps: [], debriefs: [] });
      setArtifactsLoadFailed(true);
    } finally {
      setArtifactsLoading(false);
    }
  }, [folderPath]);

  useEffect(() => {
    if (!opened) return;
    void refreshNotes();
    void refreshArtifacts();
  }, [opened, refreshNotes, refreshArtifacts]);

  const handleRowError = useCallback(
    async (action: string, error: unknown) => {
      const f = explainError(action, error);
      setFlash(f);
      if (f.kind === "info") await refreshNotes();
    },
    [refreshNotes],
  );

  const prepCount = artifacts?.preps.length ?? 0;
  const debriefCount = artifacts?.debriefs.length ?? 0;
  const notesCount = notesEntries.length;

  return (
    <Drawer
      opened={opened}
      onClose={onClose}
      title={position ? `${company} · ${position}` : company}
      position="right"
      size="lg"
      styles={{ title: { fontWeight: 600 } }}
    >
      <Stack gap="md">
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

        <Tabs value={activeTab} onChange={(v) => v && setActiveTab(v as TabKey)} variant="default">
          <Tabs.List>
            <Tabs.Tab value="notes" rightSection={<TabCount n={notesCount} />}>
              Notes
            </Tabs.Tab>
            <Tabs.Tab value="research">Research</Tabs.Tab>
            <Tabs.Tab value="prep" rightSection={<TabCount n={prepCount} />}>
              Prep
            </Tabs.Tab>
            <Tabs.Tab value="debriefs" rightSection={<TabCount n={debriefCount} />}>
              Debriefs
            </Tabs.Tab>
          </Tabs.List>

          <Tabs.Panel value="notes" pt="md">
            <NotesTab
              folderPath={folderPath}
              entries={notesEntries}
              loading={notesLoading}
              loadFailed={notesLoadFailed}
              refresh={refreshNotes}
              onError={handleRowError}
              onAddError={(e) => setFlash(explainError("add the note", e))}
            />
          </Tabs.Panel>

          <Tabs.Panel value="research" pt="md">
            <ArtifactWrap loading={artifactsLoading} loadFailed={artifactsLoadFailed}>
              <ResearchTab research={artifacts?.research ?? null} />
            </ArtifactWrap>
          </Tabs.Panel>

          <Tabs.Panel value="prep" pt="md">
            <ArtifactWrap loading={artifactsLoading} loadFailed={artifactsLoadFailed}>
              <PrepTab preps={artifacts?.preps ?? []} company={company} />
            </ArtifactWrap>
          </Tabs.Panel>

          <Tabs.Panel value="debriefs" pt="md">
            <ArtifactWrap loading={artifactsLoading} loadFailed={artifactsLoadFailed}>
              <DebriefsTab debriefs={artifacts?.debriefs ?? []} />
            </ArtifactWrap>
          </Tabs.Panel>
        </Tabs>
      </Stack>
    </Drawer>
  );
}

// -- Shared --------------------------------------------------------------------

function TabCount({ n }: { n: number }) {
  if (n === 0) return null;
  return (
    <Badge size="xs" variant="light" circle>
      {n}
    </Badge>
  );
}

function ArtifactWrap({
  loading,
  loadFailed,
  children,
}: {
  loading: boolean;
  loadFailed: boolean;
  children: React.ReactNode;
}) {
  if (loading) return <Loader size="sm" />;
  if (loadFailed) {
    return (
      <Alert variant="light" color="yellow" radius="md">
        Couldn't load artifacts — check the dashboard server and try reopening.
      </Alert>
    );
  }
  return <>{children}</>;
}

function Markdown({ children }: { children: string }) {
  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]} components={briefMdComponents}>
      {children}
    </ReactMarkdown>
  );
}

function EmptyState({
  message,
  cliHint,
}: {
  message: string;
  cliHint?: string;
}) {
  return (
    <Stack gap="xs">
      <Text size="sm" c="dimmed">{message}</Text>
      {cliHint && (
        <Text size="sm" c="dimmed">
          Run <Code>{cliHint}</Code> in your terminal.
        </Text>
      )}
    </Stack>
  );
}

// -- Research tab --------------------------------------------------------------

function ResearchTab({ research }: { research: string | null }) {
  if (!research) {
    return (
      <EmptyState
        message="No research brief yet."
        cliHint="/evaluate-position <link>"
      />
    );
  }
  return <Markdown>{research}</Markdown>;
}

// -- Prep tab ------------------------------------------------------------------

function PrepTab({ preps, company }: { preps: PrepDoc[]; company: string }) {
  if (preps.length === 0) {
    return (
      <EmptyState
        message="No prep docs for this company yet."
        cliHint={`/interview-prep ${company}`}
      />
    );
  }
  return (
    <Stack gap="lg">
      {preps.map((p) => (
        <Stack key={p.filename} gap={4}>
          <Text size="xs" fw={500} c="dimmed">{p.date}</Text>
          <Markdown>{p.markdown}</Markdown>
        </Stack>
      ))}
    </Stack>
  );
}

// -- Debriefs tab --------------------------------------------------------------

function DebriefsTab({ debriefs }: { debriefs: DebriefDoc[] }) {
  if (debriefs.length === 0) {
    return (
      <EmptyState
        message="No debriefs yet."
        cliHint="/interview-analysis"
      />
    );
  }
  return (
    <Stack gap="lg">
      {debriefs.map((d) => (
        <Stack key={d.filename} gap={4}>
          <Group gap="xs" align="baseline">
            <Text size="xs" fw={500} c="dimmed">{d.date}</Text>
            <Badge variant="light" size="sm">{d.stage}</Badge>
          </Group>
          <Markdown>{d.markdown}</Markdown>
        </Stack>
      ))}
    </Stack>
  );
}

// -- Notes tab (the existing UI, lifted into a sub-component) ------------------

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

interface NotesTabProps {
  folderPath: string;
  entries: Entry[];
  loading: boolean;
  loadFailed: boolean;
  refresh: () => Promise<void>;
  onError: (action: string, error: unknown) => Promise<void>;
  onAddError: (error: unknown) => void;
}

function NotesTab({
  folderPath,
  entries,
  loading,
  loadFailed,
  refresh,
  onError,
  onAddError,
}: NotesTabProps) {
  const [note, setNote] = useState("");
  const [saving, setSaving] = useState(false);

  const submit = async () => {
    if (!note.trim()) return;
    setSaving(true);
    try {
      await postNote(folderPath, note);
      setNote("");
      await refresh();
    } catch (e) {
      onAddError(e);
    } finally {
      setSaving(false);
    }
  };

  return (
    <Stack gap="md">
      {loadFailed && (
        <Alert variant="light" color="yellow" radius="md">
          Couldn't load notes for this position — showing an empty list.
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

      {loading && <Loader size="sm" />}
      {!loading && entries.length === 0 && (
        <Text size="sm" c="dimmed">No notes yet.</Text>
      )}
      {!loading && entries.map((entry, i) => (
        <EntryRow
          key={`${entry.fileIndex}-${entry.heading}`}
          folderPath={folderPath}
          entry={entry}
          onChange={refresh}
          onError={onError}
          isLast={i === entries.length - 1}
        />
      ))}
    </Stack>
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
