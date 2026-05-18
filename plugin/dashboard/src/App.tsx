import { Alert, Container, Loader, Stack } from "@mantine/core";
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
      <Container size="lg" py="md">
        <Alert color="red" title="Failed to load dashboard state">{error}</Alert>
      </Container>
    );
  }
  if (!state) {
    return (
      <Container size="lg" py="md">
        <Loader />
      </Container>
    );
  }

  return (
    <Container size="lg" py="md">
      <Stack gap="md">
        <PipelineStats companies={state.companies} strategy={state.strategy} />
        <ApplicationsTable
          companies={state.companies}
          onChange={refresh}
        />
        <TodaySection brief={state.latest_brief} />
      </Stack>
    </Container>
  );
}
