import { Alert, Box, Container, Grid, Loader } from "@mantine/core";
import { useCallback, useEffect, useState } from "react";

import { fetchState } from "./api";
import { ApplicationsTable } from "./components/ApplicationsTable";
import { PipelineStats } from "./components/PipelineStats";
import { TodaySection } from "./components/TodaySection";
import type { DashboardState } from "./types";

export function App() {
  const [state, setState] = useState<DashboardState | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const next = await fetchState();
      setState(next);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "unknown error");
    }
  }, []);

  useEffect(() => {
    void refresh();
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
          <ApplicationsTable companies={state.companies} onChange={refresh} />
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
