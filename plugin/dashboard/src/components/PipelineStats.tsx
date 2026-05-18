import { Group, Paper, Progress, Stack, Text } from "@mantine/core";
import { useMemo } from "react";

import type { Position, Strategy } from "../types";

interface Props {
  companies: Position[];
  strategy: Strategy;
}

const ACTIVE_STATUSES = ["interviewing", "applied", "discovered"];

export function PipelineStats({ companies, strategy }: Props) {
  const counts = useMemo(() => {
    const out = new Map<string, number>();
    for (const status of ACTIVE_STATUSES) out.set(status, 0);
    for (const p of companies) {
      if (out.has(p.status)) out.set(p.status, out.get(p.status)! + 1);
    }
    return out;
  }, [companies]);

  const weeklyBar = useMemo(() => buildWeeklyBar(companies, strategy), [companies, strategy]);
  const countdown = useMemo(() => buildCountdown(strategy.target_offer_date), [strategy.target_offer_date]);

  return (
    <Paper p="md" bg="dark.8">
      <Group justify="space-between" wrap="wrap" gap="xl">
        <Group gap="xl">
          {ACTIVE_STATUSES.map((status) => (
            <Stack gap={2} key={status}>
              <Text fz="xl" fw={700}>{counts.get(status) ?? 0}</Text>
              <Text fz="xs" c="dimmed" tt="uppercase">{status}</Text>
            </Stack>
          ))}
        </Group>
        <Group gap="xl">
          {weeklyBar && (
            <Stack gap={4} w={160}>
              <Text fz="xs" c="dimmed" tt="uppercase">{weeklyBar.label} this week</Text>
              <Text fz="lg" fw={600}>{weeklyBar.count} / {weeklyBar.target}</Text>
              <Progress value={Math.min(100, (weeklyBar.count / weeklyBar.target) * 100)} />
            </Stack>
          )}
          {countdown && (
            <Stack gap={2}>
              <Text fz="xl" fw={700}>{countdown.days}d</Text>
              <Text fz="xs" c="dimmed" tt="uppercase">to target offer</Text>
              <Text fz="xs" c="dimmed">{countdown.date}</Text>
            </Stack>
          )}
        </Group>
      </Group>
    </Paper>
  );
}

interface WeeklyBar {
  label: string;
  count: number;
  target: number;
}

function buildWeeklyBar(companies: Position[], strategy: Strategy): WeeklyBar | null {
  const targets = strategy.weekly_targets;
  if (!targets || Object.keys(targets).length === 0) return null;

  const [label, target] = Object.entries(targets).reduce((best, cur) =>
    cur[1] > best[1] ? cur : best,
  );

  const dateField = label === "applications" ? "date_applied" : "date_added";
  const start = startOfIsoWeek(new Date());
  const count = companies.filter((p) => {
    const value = p[dateField as keyof Position] as string | undefined;
    if (!value) return false;
    const t = Date.parse(value);
    return !Number.isNaN(t) && t >= start.getTime();
  }).length;

  return { label, count, target };
}

function buildCountdown(targetDate: string | undefined): { days: number; date: string } | null {
  if (!targetDate) return null;
  const t = Date.parse(targetDate);
  if (Number.isNaN(t)) return null;
  const days = Math.max(0, Math.ceil((t - Date.now()) / (24 * 60 * 60 * 1000)));
  return { days, date: targetDate };
}

function startOfIsoWeek(now: Date): Date {
  const d = new Date(now);
  const day = d.getDay() || 7;
  d.setHours(0, 0, 0, 0);
  d.setDate(d.getDate() - (day - 1));
  return d;
}
