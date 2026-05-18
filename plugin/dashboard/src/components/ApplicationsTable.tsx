import {
  Accordion,
  ActionIcon,
  Badge,
  Button,
  Group,
  SegmentedControl,
  Stack,
  Table,
  Text,
} from "@mantine/core";
import { IconCopy, IconExternalLink, IconNote, IconPlus } from "@tabler/icons-react";
import { useMemo, useState } from "react";

import type { Position } from "../types";
import { NewCompanyModal } from "./NewCompanyModal";
import { NoteDrawer } from "./NoteDrawer";
import { StatusSelect } from "./StatusSelect";

type GroupKey = "Status" | "Tier";

interface Props {
  companies: Position[];
  userdataRoot: string;
  onChange: () => void;
}

const TIER_COLORS: Record<string, string> = {
  P0: "red",
  P1: "orange",
  P2: "gray",
  P3: "gray",
};

export function ApplicationsTable({ companies, userdataRoot, onChange }: Props) {
  const [groupBy, setGroupBy] = useState<GroupKey>("Status");
  const [modalOpen, setModalOpen] = useState(false);
  const [notePosition, setNotePosition] = useState<Position | null>(null);

  const groups = useMemo(() => buildGroups(companies, groupBy), [companies, groupBy]);

  return (
    <Stack gap="md">
      <Group justify="space-between">
        <SegmentedControl
          data={["Status", "Tier"]}
          value={groupBy}
          onChange={(v) => setGroupBy(v as GroupKey)}
        />
        <Button leftSection={<IconPlus size={16} />} onClick={() => setModalOpen(true)}>
          New company
        </Button>
      </Group>

      <Accordion multiple defaultValue={groups.map((g) => g.key)}>
        {groups.map((group) => (
          <Accordion.Item key={group.key} value={group.key}>
            <Accordion.Control>
              <Group gap="sm">
                <Text fw={600}>{group.label}</Text>
                <Badge variant="light">{group.rows.length}</Badge>
              </Group>
            </Accordion.Control>
            <Accordion.Panel>
              <Table striped highlightOnHover verticalSpacing="xs">
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Tier</Table.Th>
                    <Table.Th>Company</Table.Th>
                    <Table.Th>Position</Table.Th>
                    <Table.Th>Status</Table.Th>
                    <Table.Th>Last activity</Table.Th>
                    <Table.Th />
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {group.rows.map((p) => (
                    <Table.Tr key={p.folder_path}>
                      <Table.Td>
                        <Badge color={TIER_COLORS[p.tier] ?? "gray"}>{p.tier}</Badge>
                      </Table.Td>
                      <Table.Td>
                        <Text fw={600}>{p.company}</Text>
                      </Table.Td>
                      <Table.Td>{p.position}</Table.Td>
                      <Table.Td>
                        <StatusSelect
                          folderPath={p.folder_path}
                          current={p.status}
                          onChange={onChange}
                        />
                      </Table.Td>
                      <Table.Td>
                        <Text size="xs" c="dimmed">{relativeDate(p.last_inbound ?? p.date_applied ?? p.date_added)}</Text>
                      </Table.Td>
                      <Table.Td>
                        <Group gap={4}>
                          <ActionIcon variant="subtle" aria-label="Add note" onClick={() => setNotePosition(p)}>
                            <IconNote size={16} />
                          </ActionIcon>
                          <ActionIcon
                            variant="subtle"
                            component="a"
                            href={`vscode://file/${absolutePath(userdataRoot, p.folder_path)}`}
                            aria-label="Open in VS Code"
                            title="Open in VS Code"
                          >
                            <IconExternalLink size={16} />
                          </ActionIcon>
                          <ActionIcon
                            variant="subtle"
                            aria-label="Copy meta.md path"
                            title="Copy meta.md path"
                            onClick={() => {
                              void navigator.clipboard.writeText(absolutePath(userdataRoot, p.folder_path));
                            }}
                          >
                            <IconCopy size={16} />
                          </ActionIcon>
                        </Group>
                      </Table.Td>
                    </Table.Tr>
                  ))}
                </Table.Tbody>
              </Table>
            </Accordion.Panel>
          </Accordion.Item>
        ))}
      </Accordion>

      <NewCompanyModal
        opened={modalOpen}
        onClose={() => setModalOpen(false)}
        onCreated={onChange}
      />
      <NoteDrawer
        opened={notePosition !== null}
        onClose={() => setNotePosition(null)}
        folderPath={notePosition?.folder_path ?? ""}
        company={notePosition?.company ?? ""}
        position={notePosition?.position ?? ""}
      />
    </Stack>
  );
}

interface GroupBucket {
  key: string;
  label: string;
  rows: Position[];
}

const STATUS_ORDER = [
  "interviewing",
  "applied",
  "discovered",
  "offer-received",
  "paused",
  "withdrew",
  "rejected",
];
const TIER_ORDER = ["P0", "P1", "P2", "P3"];

function buildGroups(rows: Position[], groupBy: GroupKey): GroupBucket[] {
  const buckets = new Map<string, Position[]>();
  for (const row of rows) {
    const key = groupBy === "Status" ? row.status : row.tier;
    if (!buckets.has(key)) buckets.set(key, []);
    buckets.get(key)!.push(row);
  }
  const order = groupBy === "Status" ? STATUS_ORDER : TIER_ORDER;
  const ordered: GroupBucket[] = [];
  for (const key of order) {
    if (buckets.has(key)) {
      ordered.push({ key, label: key, rows: buckets.get(key)! });
      buckets.delete(key);
    }
  }
  for (const [key, value] of buckets.entries()) {
    ordered.push({ key, label: key, rows: value });
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

function absolutePath(userdataRoot: string, folderPath: string): string {
  // userdataRoot comes from /api/state and is the server-resolved absolute path
  // to userdata/. vscode://file/ requires absolute paths to open files reliably.
  return `${userdataRoot}/companies/${folderPath}/meta.md`;
}
