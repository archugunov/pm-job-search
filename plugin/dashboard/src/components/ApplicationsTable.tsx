import {
  Accordion,
  Badge,
  Button,
  Group,
  SegmentedControl,
  Stack,
  Table,
  Text,
} from "@mantine/core";
import { IconPlus } from "@tabler/icons-react";
import { useMemo, useState } from "react";

import type { Position } from "../types";
import { NoteDrawer } from "./NoteDrawer";
import { StatusSelect } from "./StatusSelect";

type GroupKey = "Status" | "Tier";

interface Props {
  companies: Position[];
  onChange: () => void;
}

const TIER_COLORS: Record<string, string> = {
  P0: "red",
  P1: "orange",
  P2: "gray",
  P3: "gray",
};

export function ApplicationsTable({ companies, onChange }: Props) {
  const [groupBy, setGroupBy] = useState<GroupKey>("Status");
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
        <Text size="xs" c="dimmed">
          New positions land via <Text component="code">/pm-job-search:evaluate-position &lt;link&gt;</Text>
        </Text>
      </Group>

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
              <Group gap="sm" align="baseline">
                <Text fz="lg" fw={700} tt="capitalize">{group.label}</Text>
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
                    <Table.Th w={60}>Tier</Table.Th>
                    <Table.Th>Company</Table.Th>
                    <Table.Th>Position</Table.Th>
                    <Table.Th w={150}>Status</Table.Th>
                    <Table.Th w={80}>Last activity</Table.Th>
                    <Table.Th w={90} />
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {group.rows.map((p) => (
                    <Table.Tr
                      key={p.folder_path}
                      style={{ cursor: "pointer" }}
                      onClick={() => setNotePosition(p)}
                    >
                      <Table.Td>
                        {p.tier
                          ? <Badge color={TIER_COLORS[p.tier] ?? "gray"}>{p.tier}</Badge>
                          : <Text size="xs" c="dimmed">?</Text>}
                      </Table.Td>
                      <Table.Td>
                        <Text fw={600}>{p.company}</Text>
                      </Table.Td>
                      <Table.Td>
                        <Text>{p.position || <Text component="span" c="dimmed">(pending)</Text>}</Text>
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
                      <Table.Td>
                        <Button
                          size="xs"
                          variant="light"
                          radius="xl"
                          leftSection={<IconPlus size={12} />}
                          onClick={(e) => {
                            e.stopPropagation();
                            setNotePosition(p);
                          }}
                        >
                          note
                        </Button>
                      </Table.Td>
                    </Table.Tr>
                  ))}
                </Table.Tbody>
              </Table>
            </Accordion.Panel>
          </Accordion.Item>
        ))}
      </Accordion>

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

const STATUS_ORDER = ["new", "interviewing", "applied", "offer", "rejected", "closed"];
const TIER_ORDER = ["P0", "P1", "P2", "P3"];

function buildGroups(rows: Position[], groupBy: GroupKey): GroupBucket[] {
  const buckets = new Map<string, Position[]>();
  for (const row of rows) {
    const key = groupBy === "Status" ? (row.status || "—") : (row.tier || "—");
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
