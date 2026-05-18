import { Alert, Container, Grid, Loader, Stack } from "@mantine/core";
import { useCallback, useEffect, useMemo, useState } from "react";

import { fetchState } from "./api";
import { ApplicationsTable } from "./components/ApplicationsTable";
import { InsightsCard } from "./components/InsightsCard";
import { PipelineStats } from "./components/PipelineStats";
import { TodaySection } from "./components/TodaySection";
import { extractSection } from "./components/briefMarkdown";
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

  const headsUp = useMemo(() => {
    if (!state?.latest_brief) return null;
    return extractSection(state.latest_brief.markdown, /^##\s+heads[-\s]?up/i);
  }, [state?.latest_brief]);

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
      <Stack gap="md">
        <Grid gutter="md">
          <Grid.Col span={{ base: 12, md: 6 }}>
            <Stack gap="md">
              <PipelineStats companies={state.companies} strategy={state.strategy} />
              {headsUp && <InsightsCard markdown={headsUp} />}
            </Stack>
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 6 }}>
            <TodaySection brief={state.latest_brief} />
          </Grid.Col>
        </Grid>
        <ApplicationsTable companies={state.companies} onChange={refresh} />
      </Stack>
    </Container>
  );
}
