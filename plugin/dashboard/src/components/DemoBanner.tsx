import { Anchor, Box, Button, Container, Group, Text } from "@mantine/core";
import { IconBrandGithub } from "@tabler/icons-react";
import { useState } from "react";

import { REPO_URL } from "../config";
import { AboutDialog } from "./AboutDialog";
import { ClaudeIcon } from "./ClaudeIcon";
import "./DemoBanner.css";

export function DemoBanner() {
  const [aboutOpen, setAboutOpen] = useState(false);

  return (
    <>
      <Box
        py="xs"
        style={{
          borderBottom: "1px solid #E5BFA0",
          background: "#FBE6D4",
          color: "var(--mantine-color-dark-9)",
        }}
      >
        <Container size="xl">
          <Group justify="space-between" wrap="nowrap" gap="md">
            <Text size="sm" fw={500} style={{ lineHeight: 1.4, color: "var(--mantine-color-dark-9)" }}>
              Live demo of <strong>pm-job-search</strong>, an open-source <ClaudeIcon size={14} />Claude
              Code plugin for senior product leaders running a job search.
            </Text>
            <Group gap="xs" wrap="nowrap">
              <Button
                size="xs"
                variant="filled"
                onClick={() => setAboutOpen(true)}
                styles={{ root: { backgroundColor: "#000", color: "#fff" } }}
              >
                Learn more
              </Button>
              <Anchor href={REPO_URL} target="_blank" rel="noopener noreferrer" underline="never">
                <Button
                  size="xs"
                  variant="subtle"
                  leftSection={<IconBrandGithub size={14} />}
                  className="banner-github-btn"
                >
                  GitHub
                </Button>
              </Anchor>
            </Group>
          </Group>
        </Container>
      </Box>
      <AboutDialog opened={aboutOpen} onClose={() => setAboutOpen(false)} />
    </>
  );
}
