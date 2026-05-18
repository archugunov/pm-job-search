import { Code, Divider, Group, Paper, Stack, Text } from "@mantine/core";
import { useMemo } from "react";

import type { Position, Strategy, WeeklyProgress } from "../types";
import { statusLabel } from "../statusColors";

interface Props {
  companies: Position[];
  strategy: Strategy;
  weeklyProgress: WeeklyProgress;
}

// Hero counters in display order. `offer` first because an offer in hand is
// the highest-signal Active state — a decision is imminent, surface it most.
// Matches the offer-first sort in /today's pipeline-state group order.
const HERO_STATUSES = ["offer", "interviewing", "applied"];

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
  const noStrategyTracking = !countdown && weeklyBars.length === 0;

  return (
    <Paper p="md" radius="lg" bg="dark.8">
      <Stack gap="md">
        <Group grow wrap="nowrap" gap={0}>
          {HERO_STATUSES.map((status) => {
            const count = counts.get(status) ?? 0;
            // Offer counter dimmed at 0 (it's the rare state), bright when it fires.
            const isHighlight = status === "offer" && count > 0;
            return (
              <Stack gap={2} key={status} align="flex-start">
                <Text
                  fz={26}
                  fw={700}
                  lh={1}
                  c={isHighlight ? "green.4" : undefined}
                >
                  {count}
                </Text>
                <Text fz="xs" c="dimmed" tt="uppercase">{statusLabel(status)}</Text>
              </Stack>
            );
          })}
          {countdown && (
            <Stack gap={2} align="flex-start">
              <Text fz={26} fw={700} lh={1}>{countdown.days}</Text>
              <Text fz="xs" c="dimmed" tt="uppercase">days left</Text>
            </Stack>
          )}
        </Group>

        {weeklyBars.length > 0 && (
          <>
            <Divider />
            <Stack gap={6}>
              <Text fz="xs" c="dimmed" tt="uppercase" fw={600}>
                This week (day {weeklyProgress.window_days}/7)
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

        {noStrategyTracking && (
          <>
            <Divider />
            <Text fz="xs" c="dimmed">
              No strategy set. Run <Code>/pm-job-search:setup</Code> to enable
              countdown + weekly targets.
            </Text>
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
