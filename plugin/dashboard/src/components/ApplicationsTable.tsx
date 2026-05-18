import {
  Accordion,
  ActionIcon,
  Badge,
  Box,
  Button,
  Code,
  Group,
  Paper,
  Popover,
  Stack,
  Table,
  Text,
  Textarea,
  Tooltip,
} from "@mantine/core";
import { useHover } from "@mantine/hooks";
import { IconCheck, IconExternalLink, IconPencilPlus } from "@tabler/icons-react";
import { useEffect, useMemo, useRef, useState } from "react";

import { postNote } from "../api";
import type { Position } from "../types";
import { STATUS_KEYS, statusColor, statusLabel } from "../statusColors";
import { CompanyDrawer } from "./CompanyDrawer";
import { StatusSelect } from "./StatusSelect";

interface Props {
  companies: Position[];
  onChange: () => void;
}

const TIER_COLORS: Record<string, string> = {
  P0: "red",
  P1: "yellow",
  P2: "gray",
  P3: "gray",
};


export function ApplicationsTable({ companies, onChange }: Props) {
  const [notePosition, setNotePosition] = useState<Position | null>(null);

  const groups = useMemo(() => buildGroups(companies), [companies]);

  if (groups.length === 0) {
    return (
      <Paper p="xl" radius="lg" bg="dark.8">
        <Stack gap="sm" align="flex-start">
          <Text fz="lg" fw={600}>No companies yet.</Text>
          <Text size="sm" c="dimmed">
            Run <Code>/pm-job-search:setup</Code> first, then add your first role with{" "}
            <Code>/pm-job-search:evaluate-position &lt;link&gt;</Code> in Claude Code.
          </Text>
          <Text size="sm" c="dimmed">
            Once positions land in <Code>userdata/companies/</Code>, they show up here automatically.
          </Text>
        </Stack>
      </Paper>
    );
  }

  return (
    <Stack gap="md">
      <Accordion
        multiple
        variant="separated"
        radius="lg"
        defaultValue={groups.map((g) => g.key)}
        styles={{
          item: {
            backgroundColor: "var(--mantine-color-dark-8)",
            border: "none",
          },
        }}
      >
        {groups.map((group) => (
          <Accordion.Item key={group.key} value={group.key}>
            <Accordion.Control>
              <Group gap="sm" align="center">
                <Box
                  w={10}
                  h={10}
                  style={{
                    borderRadius: "50%",
                    backgroundColor: statusColor(group.key),
                    flexShrink: 0,
                  }}
                />
                <Text fz="lg" fw={700}>{group.label}</Text>
                <Badge variant="light" size="lg">{group.rows.length}</Badge>
              </Group>
            </Accordion.Control>
            <Accordion.Panel>
              <Table
                highlightOnHover
                highlightOnHoverColor="dark.7"
                verticalSpacing="xs"
                layout="fixed"
              >
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th w={70}>Tier</Table.Th>
                    <Table.Th>Company / Position</Table.Th>
                    <Table.Th w={165}>Status</Table.Th>
                    <Table.Th w={70}>Last</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {group.rows.map((p) => (
                    <PositionRow
                      key={p.folder_path}
                      p={p}
                      onOpen={setNotePosition}
                      onChange={onChange}
                    />
                  ))}
                </Table.Tbody>
              </Table>
            </Accordion.Panel>
          </Accordion.Item>
        ))}
      </Accordion>

      <CompanyDrawer
        opened={notePosition !== null}
        onClose={() => setNotePosition(null)}
        folderPath={notePosition?.folder_path ?? ""}
        company={notePosition?.company ?? ""}
        position={notePosition?.position ?? ""}
        hasNotes={notePosition?.has_notes ?? false}
        link={notePosition?.link}
      />
    </Stack>
  );
}

interface PositionRowProps {
  p: Position;
  onOpen: (p: Position) => void;
  onChange: () => void;
}

function PositionRow({ p, onOpen, onChange }: PositionRowProps) {
  const { hovered, ref } = useHover<HTMLTableRowElement>();
  const [popoverOpen, setPopoverOpen] = useState(false);
  const showAction = hovered || popoverOpen;

  return (
    <Table.Tr
      ref={ref as React.LegacyRef<HTMLTableRowElement>}
      style={{ cursor: "pointer" }}
      onClick={() => onOpen(p)}
    >
      <Table.Td>
        {p.tier
          ? <Badge color={TIER_COLORS[p.tier] ?? "gray"}>{p.tier}</Badge>
          : (
            <Tooltip
              label="Tier unset — run /pm-job-search:evaluate-position to score this role"
              withArrow
              position="right"
            >
              <Text size="xs" c="dimmed" style={{ cursor: "help" }}>?</Text>
            </Tooltip>
          )}
      </Table.Td>
      <Table.Td>
        <Group gap="xs" align="center" wrap="nowrap">
          <Stack gap={0} style={{ minWidth: 0 }}>
            <Text fw={600} truncate>{p.company}</Text>
            <Text size="xs" c="dimmed" truncate>{p.position || "(pending)"}</Text>
          </Stack>
          <Box onClick={(e) => e.stopPropagation()} style={{ flexShrink: 0, lineHeight: 0, display: "flex", gap: 8 }}>
            <OpenPostingIcon link={p.link} company={p.company} visible={showAction} />
            <QuickAddNote
              folderPath={p.folder_path}
              company={p.company}
              visible={showAction}
              opened={popoverOpen}
              onChange={setPopoverOpen}
              onAdded={onChange}
            />
          </Box>
        </Group>
      </Table.Td>
      <Table.Td onClick={(e) => e.stopPropagation()}>
        <StatusSelect
          folderPath={p.folder_path}
          current={p.status}
          onChange={onChange}
        />
      </Table.Td>
      <Table.Td>
        <Text size="xs" c="dimmed">{relativeDate(p.last_inbound ?? p.date_applied ?? p.date_added)}</Text>
      </Table.Td>
    </Table.Tr>
  );
}

interface OpenPostingIconProps {
  link: string | undefined;
  company: string;
  visible: boolean;
}

function OpenPostingIcon({ link, company, visible }: OpenPostingIconProps) {
  if (!link) {
    // Reserve the slot so the pencil doesn't jump horizontally between rows.
    return <Box w={28} h={28} />;
  }
  return (
    <Tooltip label="Open posting" openDelay={400} withArrow>
      <ActionIcon
        component="a"
        href={link}
        target="_blank"
        rel="noopener noreferrer"
        size="lg"
        variant="subtle"
        color="gray"
        radius="xl"
        onClick={(e) => e.stopPropagation()}
        aria-label={`Open posting for ${company} in new tab`}
        style={{
          opacity: visible ? 1 : 0,
          pointerEvents: visible ? "auto" : "none",
          transition: "opacity 140ms ease",
        }}
      >
        <IconExternalLink size={18} stroke={1.4} />
      </ActionIcon>
    </Tooltip>
  );
}

interface QuickAddNoteProps {
  folderPath: string;
  company: string;
  visible: boolean;
  opened: boolean;
  onChange: (opened: boolean) => void;
  onAdded: () => void;
}

function QuickAddNote({ folderPath, company, visible, opened, onChange, onAdded }: QuickAddNoteProps) {
  const [note, setNote] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [savedFlash, setSavedFlash] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (opened) {
      // Defer focus a tick — Popover mounts the dropdown asynchronously.
      const t = setTimeout(() => textareaRef.current?.focus(), 0);
      return () => clearTimeout(t);
    }
    setNote("");
    setError(null);
  }, [opened]);

  const submit = async () => {
    if (!note.trim() || saving) return;
    setSaving(true);
    setError(null);
    try {
      await postNote(folderPath, note);
      setNote("");
      onChange(false);
      // Pencil morphs to a green check for ~900ms, then back.
      setSavedFlash(true);
      window.setTimeout(() => setSavedFlash(false), 900);
      onAdded();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setSaving(false);
    }
  };

  // Keep the icon visible during the saved flash even if the row isn't hovered
  // and the popover has closed — otherwise the morph would happen on a hidden
  // button.
  const showIcon = visible || savedFlash;

  return (
    <Popover
      opened={opened}
      onChange={onChange}
      position="bottom-end"
      withArrow
      shadow="md"
      radius="md"
      width={320}
      trapFocus
    >
      <Popover.Target>
        <Tooltip label="Add a note" openDelay={400} withArrow disabled={opened || savedFlash}>
          <ActionIcon
            size="lg"
            variant={savedFlash ? "light" : "subtle"}
            color={savedFlash ? "green" : "gray"}
            radius="xl"
            onClick={(e) => {
              e.stopPropagation();
              if (savedFlash) return;
              onChange(!opened);
            }}
            aria-label={savedFlash ? "Saved" : `Add a note about ${company}`}
            style={{
              opacity: showIcon ? 1 : 0,
              pointerEvents: showIcon ? "auto" : "none",
              transition: "opacity 140ms ease, background-color 200ms ease, color 200ms ease",
            }}
          >
            {savedFlash ? (
              <IconCheck size={18} stroke={2} />
            ) : (
              <IconPencilPlus size={18} stroke={1.4} />
            )}
          </ActionIcon>
        </Tooltip>
      </Popover.Target>
      <Popover.Dropdown onClick={(e) => e.stopPropagation()}>
        <Stack gap="xs">
          <Textarea
            ref={textareaRef}
            autosize
            minRows={3}
            radius="md"
            placeholder={`What's new with ${company}?`}
            value={note}
            onChange={(e) => setNote(e.currentTarget.value)}
            disabled={saving}
            onKeyDown={(e) => {
              if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
                e.preventDefault();
                void submit();
              } else if (e.key === "Escape") {
                e.preventDefault();
                onChange(false);
              }
            }}
          />
          {error && <Text size="xs" c="red">{error}</Text>}
          <Group justify="space-between" align="center">
            <Text size="xs" c="dimmed">⌘↵ to save · esc to cancel</Text>
            <Button
              size="xs"
              radius="md"
              loading={saving}
              onClick={submit}
              disabled={!note.trim()}
            >
              Add note
            </Button>
          </Group>
        </Stack>
      </Popover.Dropdown>
    </Popover>
  );
}

interface GroupBucket {
  key: string;
  label: string;
  rows: Position[];
}

function buildGroups(rows: Position[]): GroupBucket[] {
  const buckets = new Map<string, Position[]>();
  for (const row of rows) {
    const key = row.status || "—";
    if (!buckets.has(key)) buckets.set(key, []);
    buckets.get(key)!.push(row);
  }
  const ordered: GroupBucket[] = [];
  for (const key of STATUS_KEYS) {
    if (buckets.has(key)) {
      ordered.push({ key, label: statusLabel(key), rows: buckets.get(key)! });
      buckets.delete(key);
    }
  }
  for (const [key, value] of buckets.entries()) {
    ordered.push({ key, label: statusLabel(key), rows: value });
  }
  return ordered;
}

function relativeDate(iso: string | undefined): string {
  if (!iso) return "—";
  const then = Date.parse(iso);
  if (Number.isNaN(then)) return iso;
  const days = Math.floor((Date.now() - then) / (24 * 60 * 60 * 1000));
  if (days < 1) return "today";
  if (days < 2) return "1d";
  if (days < 7) return `${days}d`;
  if (days < 14) return "1w";
  if (days < 60) return `${Math.floor(days / 7)}w`;
  return `${Math.floor(days / 30)}mo`;
}
