import { Alert, Box, Container, Grid, Loader } from "@mantine/core";
import { useCallback, useEffect, useRef, useState } from "react";

import { fetchState } from "./api";
import { ApplicationsTable } from "./components/ApplicationsTable";
import { PipelineStats } from "./components/PipelineStats";
import { TodaySection } from "./components/TodaySection";
import type { DashboardState } from "./types";

// Poll the state endpoint while the tab is visible so the dashboard
// reflects CLI mutations (/today, /evaluate-position, /interview-analysis)
// without manual page reloads. 5s is the sweet spot — feels live, payload
// is small, and matches the cadence at which a user typically switches
// terminal → browser after running a skill.
const POLL_INTERVAL_MS = 5000;

export function App() {
  const [state, setState] = useState<DashboardState | null>(null);
  const [error, setError] = useState<string | null>(null);
  // Tracks in-flight requests so visibility-change refresh doesn't double-fire
  // mid-poll. Cheap belt-and-braces — fetch() would dedupe at the network
  // layer anyway, but this avoids racing setState calls.
  const inFlight = useRef(false);

  const refresh = useCallback(async () => {
    if (inFlight.current) return;
    inFlight.current = true;
    try {
      const next = await fetchState();
      setState(next);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "unknown error");
    } finally {
      inFlight.current = false;
    }
  }, []);

  // Initial fetch.
  useEffect(() => {
    void refresh();
  }, [refresh]);

  // Visibility-aware polling. When the tab is hidden, we stop polling so
  // background tabs don't hammer the server. On becoming visible again we
  // refresh immediately (the user just switched back — probably to check
  // something that just happened) and resume the interval.
  useEffect(() => {
    let interval: number | null = null;

    const start = () => {
      if (interval !== null) return;
      interval = window.setInterval(() => {
        if (document.visibilityState === "visible") void refresh();
      }, POLL_INTERVAL_MS);
    };

    const stop = () => {
      if (interval === null) return;
      window.clearInterval(interval);
      interval = null;
    };

    const handleVisibility = () => {
      if (document.visibilityState === "visible") {
        void refresh();
        start();
      } else {
        stop();
      }
    };

    document.addEventListener("visibilitychange", handleVisibility);
    if (document.visibilityState === "visible") start();

    return () => {
      document.removeEventListener("visibilitychange", handleVisibility);
      stop();
    };
  }, [refresh]);

  if (error) {
    return (
      <Container size="xl" py="md">
        <Alert color="red" title="Failed to load dashboard state">{error}</Alert>
      </Container>
    );
  }
  if (!state) {
    return (
      <Container size="xl" py="md">
        <Loader />
      </Container>
    );
  }

  return (
    <Container size="xl" py="md">
      <Grid gutter="md">
        <Grid.Col span={{ base: 12, md: 8 }}>
          <Box
            style={{
              position: "sticky",
              top: 16,
              height: "calc(100vh - 32px)",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <Box style={{ flex: 1, minHeight: 0, overflowY: "auto" }}>
              <ApplicationsTable companies={state.companies} onChange={refresh} />
            </Box>
          </Box>
        </Grid.Col>
        <Grid.Col span={{ base: 12, md: 4 }}>
          <Box
            style={{
              position: "sticky",
              top: 16,
              height: "calc(100vh - 32px)",
              display: "flex",
              flexDirection: "column",
              gap: 16,
            }}
          >
            <PipelineStats
              companies={state.companies}
              strategy={state.strategy}
              weeklyProgress={state.weekly_progress}
            />
            <Box style={{ flex: 1, minHeight: 0 }}>
              <TodaySection brief={state.latest_brief} />
            </Box>
          </Box>
        </Grid.Col>
      </Grid>
    </Container>
  );
}
