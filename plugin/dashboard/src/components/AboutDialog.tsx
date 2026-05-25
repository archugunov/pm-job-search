import { Anchor, Box, Button, Group, List, Modal, Stack, Text, Title } from "@mantine/core";
import { IconBrandGithub } from "@tabler/icons-react";

import { AUTHOR_LINKEDIN_URL, AUTHOR_NAME, INSTALL_URL, REPO_URL } from "../config";
import { ClaudeIcon } from "./ClaudeIcon";

interface Props {
  opened: boolean;
  onClose: () => void;
}

export function AboutDialog({ opened, onClose }: Props) {
  return (
    <Modal
      opened={opened}
      onClose={onClose}
      withCloseButton={false}
      size={620}
      centered
      padding={0}
      radius="lg"
      overlayProps={{ backgroundOpacity: 0.6, blur: 4 }}
      styles={{
        content: {
          boxShadow:
            "0 24px 64px -16px rgba(0, 0, 0, 0.65), 0 8px 24px -8px rgba(0, 0, 0, 0.4)",
          border: "1px solid rgba(255, 255, 255, 0.06)",
          backgroundImage:
            "linear-gradient(180deg, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0) 30%)",
          display: "flex",
          flexDirection: "column",
          maxHeight: "85vh",
        },
        body: {
          padding: 0,
          display: "flex",
          flexDirection: "column",
          minHeight: 0,
          flex: 1,
        },
      }}
    >
      <Box px="xl" pt="xl" pb="lg" style={{ flexShrink: 0 }}>
        <Stack gap={6}>
          <Title order={2} fw={600}>
            pm-job-search
          </Title>
          <Text size="sm" c="dimmed">
            A <ClaudeIcon size={12} />Claude Code plugin that runs your senior-PM job search
            end-to-end from the terminal.
          </Text>
        </Stack>
      </Box>

      <Box
        px="xl"
        py="lg"
        style={{
          borderTop: "1px solid var(--mantine-color-dark-5)",
          flex: 1,
          minHeight: 0,
          overflowY: "auto",
        }}
      >
        <Stack gap="lg">
          <Section title="What the plugin does">
            <Text size="sm" component="div" mb={8} style={{ lineHeight: 1.55 }}>
              The actual work happens through commands in Claude Code:
            </Text>
            <List size="sm" spacing={6} styles={{ itemWrapper: { lineHeight: 1.5 } }}>
              <List.Item>
                <strong>Discover & score</strong> — weekly sweep of target companies plus one-off postings
                scored against your own rubric.
              </List.Item>
              <List.Item>
                <strong>Apply</strong> — tailors your CV per role; every claim traces back to your master CV
                or your own answers.
              </List.Item>
              <List.Item>
                <strong>Interview prep</strong> — adapts stories from your STAR-story bank for each round.
              </List.Item>
              <List.Item>
                <strong>Evaluate the offer</strong> — checks comp, anti-goals, and the senior-PM archetype.
              </List.Item>
              <List.Item>
                <strong>Honest career coach</strong> — pushes back when the search itself isn't working.
              </List.Item>
            </List>
          </Section>

          <Section title="What this dashboard is">
            <Text size="sm" component="div" mb={8} style={{ lineHeight: 1.55 }}>
              An optional visual layer on top of the plugin. You open it from inside Claude Code with{" "}
              <code>/pm-job-search:dashboard</code> — it launches in your browser and reads the same files the
              plugin's other commands work with.
            </Text>
            <Text size="sm" component="div" style={{ lineHeight: 1.55 }}>
              The terminal is great for thinking-and-writing work. The dashboard is for the moments in between:
            </Text>
            <List size="sm" spacing={4} mt={6} styles={{ itemWrapper: { lineHeight: 1.5 } }}>
              <List.Item>Scanning the whole pipeline at a glance, especially with many open roles.</List.Item>
              <List.Item>Bumping a status after a recruiter call, or jotting a note between meetings.</List.Item>
              <List.Item>Reading a research brief, prep doc, or interview debrief without opening files.</List.Item>
            </List>
          </Section>

          <Section title="Yours, on your machine">
            Everything lives on your laptop — your pipeline, your notes, your interview prep. Nothing is sent
            to a server, nothing is shared with anyone, nothing leaves until you choose.
          </Section>

          <Section title="About this demo">
            You're looking at the dashboard alone, with a fictional candidate (Maya) loaded in. Status changes
            and notes work — they just live in your browser tab and reset on refresh. In a real install, those
            edits write back to your local markdown files, and the rest of the plugin reads them.
          </Section>

          <Section title="Built by">
            <Anchor href={AUTHOR_LINKEDIN_URL} target="_blank" rel="noopener noreferrer" fw={500}>
              {AUTHOR_NAME}
            </Anchor>
            <Text size="sm" c="dimmed" mt={4}>
              © {new Date().getFullYear()}
            </Text>
          </Section>
        </Stack>
      </Box>

      <Group
        justify="flex-end"
        gap="sm"
        px="xl"
        py="md"
        style={{
          borderTop: "1px solid var(--mantine-color-dark-5)",
          background: "rgba(0, 0, 0, 0.25)",
          flexShrink: 0,
          boxShadow: "0 -8px 16px -8px rgba(0, 0, 0, 0.3)",
        }}
      >
        <Anchor href={INSTALL_URL} target="_blank" rel="noopener noreferrer" underline="never">
          <Button variant="default">How to install</Button>
        </Anchor>
        <Anchor href={REPO_URL} target="_blank" rel="noopener noreferrer" underline="never">
          <Button leftSection={<IconBrandGithub size={16} />}>GitHub</Button>
        </Anchor>
      </Group>
    </Modal>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <Text
        fz="xs"
        fw={600}
        tt="uppercase"
        c="dimmed"
        mb={6}
        style={{ letterSpacing: "0.04em" }}
      >
        {title}
      </Text>
      <Text size="sm" component="div" style={{ lineHeight: 1.55 }}>
        {children}
      </Text>
    </div>
  );
}
