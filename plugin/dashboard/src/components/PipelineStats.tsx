import { Divider, Group, Paper, Stack, Text } from "@mantine/core";
import { useMemo } from "react";

import type { Position, Strategy, WeeklyProgress } from "../types";

interface Props {
  companies: Position[];
  strategy: Strategy;
  weeklyProgress: WeeklyProgress;
}

const HERO_STATUSES = ["interviewing", "applied"];

export function PipelineStats({ companies, strategy, weeklyProgress }: Props) {
  const counts = useMemo(() => {
    const out = new Map<string, number>();
    for (const status of HERO_STATUSES) out.set(status, 0);
    for (const p of companies) {
      if (out.has(p.status)) out.set(p.status, out.get(p.status)! + 1);
    }
    return out;
  }, [companies]);

  const weeklyBars = useMemo(() => buildWeeklyBars(strategy, weeklyProgress), [strategy, weeklyProgress]);
  const countdown = useMemo(() => buildCountdown(strategy.target_offer_date), [strategy.target_offer_date]);

  return (
    <Paper p="md" radius="lg" bg="dark.8">
      <Stack gap="md">
        <Group gap={48} wrap="wrap">
          {HERO_STATUSES.map((status) => (
            <Stack gap={2} key={status}>
              <Text fz={32} fw={700} lh={1}>{counts.get(status) ?? 0}</Text>
              <Text fz="xs" c="dimmed" tt="uppercase">{status}</Text>
            </Stack>
          ))}
          {countdown && (
            <Stack gap={2}>
              <Text fz={32} fw={700} lh={1}>{countdown.days}d</Text>
              <Text fz="xs" c="dimmed" tt="uppercase">to target offer</Text>
            </Stack>
          )}
        </Group>

        {weeklyBars.length > 0 && (
          <>
            <Divider />
            <Stack gap={6}>
              <Text fz="xs" c="dimmed" tt="uppercase" fw={600}>
                Last {weeklyProgress.window_days} days
              </Text>
              {weeklyBars.map((bar) => (
                <Group key={bar.label} gap="md" wrap="nowrap">
                  <Text fz="sm" w={140} c="dimmed">{prettify(bar.label)}</Text>
                  <Text fz="sm" fw={600}>{bar.count} / {bar.target}</Text>
                </Group>
              ))}
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

function buildWeeklyBars(strategy: Strategy, progress: WeeklyProgress): WeeklyBar[] {
  const targets = strategy.weekly_targets;
  if (!targets || Object.keys(targets).length === 0) return [];

  return Object.entries(targets).map(([label, target]) => {
    const count = (progress as unknown as Record<string, number>)[label] ?? 0;
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

function prettify(label: string): string {
  return label.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
