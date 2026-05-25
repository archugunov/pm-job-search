import { Alert, Box, Container, Grid, Loader, Stack } from "@mantine/core";
import { useMediaQuery } from "@mantine/hooks";
import { useCallback, useEffect, useRef, useState } from "react";

import { fetchState } from "./api";
import { ApplicationsTable } from "./components/ApplicationsTable";
import { DemoBanner } from "./components/DemoBanner";
import { MobileLanding } from "./components/MobileLanding";
import { PipelineStats } from "./components/PipelineStats";
import { TodaySection } from "./components/TodaySection";
import { DEMO_MODE } from "./config";
import type { DashboardState } from "./types";

// Poll the state endpoint while the tab is visible so the dashboard
// reflects CLI mutations (/today, /evaluate-position, /interview-analysis)
// without manual page reloads. 5s is the sweet spot — feels live, payload
// is small, and matches the cadence at which a user typically switches
// terminal → browser after running a skill.
const POLL_INTERVAL_MS = 5000;

export function App() {
  // Resolve synchronously on first render (matchMedia is available client-side
  // in this static SPA) so the mobile landing doesn't flicker through the
  // desktop layout on initial paint.
  const isMobile = useMediaQuery("(max-width: 768px)", false, {
    getInitialValueInEffect: false,
  });
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
  //
  // Polling is disabled in demo mode — there's no external process mutating
  // state, so re-fetching every 5s would just churn React for no reason.
  useEffect(() => {
    if (DEMO_MODE) return;
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

  // Demo mode on a narrow viewport: replace the whole dashboard with a
  // landing page. Claude Code is a desktop CLI, so trying to interact with
  // the live demo on a phone is pointless — show the explainer + video
  // instead and steer visitors to install on a laptop.
  if (DEMO_MODE && isMobile) {
    return <MobileLanding />;
  }

  let body;
  if (error) {
    body = (
      <Container size="xl" py="md">
        <Alert color="red" title="Failed to load dashboard state">{error}</Alert>
      </Container>
    );
  } else if (!state) {
    body = (
      <Container size="xl" py="md">
        <Loader />
      </Container>
    );
  } else if (DEMO_MODE) {
    // Demo mode: page scrolls as a single document. Columns flow naturally
    // with no sticky/full-height constraints — visitors scroll the whole page
    // to read everything, banner stays pinned via the wrapper below.
    body = (
      <Container size="xl" py="md">
        <Grid gutter="md">
          <Grid.Col span={{ base: 12, md: 8 }}>
            <ApplicationsTable companies={state.companies} onChange={refresh} />
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 4 }}>
            <Stack gap="md">
              <PipelineStats
                companies={state.companies}
                strategy={state.strategy}
                weeklyProgress={state.weekly_progress}
              />
              <TodaySection brief={state.latest_brief} />
            </Stack>
          </Grid.Col>
        </Grid>
      </Container>
    );
  } else {
    body = (
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

  return (
    <>
      {DEMO_MODE && (
        <Box style={{ position: "sticky", top: 0, zIndex: 100 }}>
          <DemoBanner />
        </Box>
      )}
      {body}
    </>
  );
}
