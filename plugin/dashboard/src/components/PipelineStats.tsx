import { Divider, Group, Paper, Progress, Stack, Text } from "@mantine/core";
import { useMemo } from "react";

import type { Position, Strategy } from "../types";

interface Props {
  companies: Position[];
  strategy: Strategy;
}

const HERO_STATUSES = ["interviewing", "applied"];

export function PipelineStats({ companies, strategy }: Props) {
  const counts = useMemo(() => {
    const out = new Map<string, number>();
    for (const status of HERO_STATUSES) out.set(status, 0);
    for (const p of companies) {
      if (out.has(p.status)) out.set(p.status, out.get(p.status)! + 1);
    }
    return out;
  }, [companies]);

  const weeklyBars = useMemo(() => buildWeeklyBars(companies, strategy), [companies, strategy]);
  const countdown = useMemo(() => buildCountdown(strategy.target_offer_date), [strategy.target_offer_date]);

  return (
    <Paper p="md" radius="lg" bg="dark.8">
      <Stack gap="md">
        <Group justify="space-between" wrap="wrap" gap="xl">
          <Group gap={48}>
            {HERO_STATUSES.map((status) => (
              <Stack gap={2} key={status}>
                <Text fz={32} fw={700} lh={1}>{counts.get(status) ?? 0}</Text>
                <Text fz="xs" c="dimmed" tt="uppercase">{status}</Text>
              </Stack>
            ))}
          </Group>
          {countdown && (
            <Stack gap={2} align="flex-end">
              <Text fz="xl" fw={700} lh={1}>{countdown.days}d</Text>
              <Text fz="xs" c="dimmed" tt="uppercase">to target offer</Text>
              <Text fz="xs" c="dimmed">{countdown.date}</Text>
            </Stack>
          )}
        </Group>

        {weeklyBars.length > 0 && (
          <>
            <Divider />
            <Stack gap="xs">
              <Text fz="xs" c="dimmed" tt="uppercase" fw={600}>This week</Text>
              {weeklyBars.map((bar) => {
                const pct = Math.min(100, (bar.count / bar.target) * 100);
                return (
                  <Group key={bar.label} gap="md" wrap="nowrap">
                    <Text fz="sm" w={140} c="dimmed">{prettify(bar.label)}</Text>
                    <Progress value={pct} style={{ flex: 1 }} radius="xl" />
                    <Text fz="sm" fw={600} w={56} ta="right">
                      {bar.count} / {bar.target}
                    </Text>
                  </Group>
                );
              })}
            </Stack>
          </>
        )}
      </Stack>
    </Paper>
  );
}

interface WeeklyBar {
  label: string;
  count: number;
  target: number;
}

function buildWeeklyBars(companies: Position[], strategy: Strategy): WeeklyBar[] {
  const targets = strategy.weekly_targets;
  if (!targets || Object.keys(targets).length === 0) return [];

  const start = startOfIsoWeek(new Date()).getTime();

  return Object.entries(targets).map(([label, target]) => {
    const dateField = label === "applications" ? "date_applied" : "date_added";
    const count = companies.filter((p) => {
      const value = p[dateField as keyof Position] as string | undefined;
      if (!value) return false;
      const t = Date.parse(value);
      return !Number.isNaN(t) && t >= start;
    }).length;
    return { label, count, target };
  });
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

function prettify(label: string): string {
  return label.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
