import { ActionIcon, Anchor, Box, Button, Container, Group, List, Stack, Text, Title } from "@mantine/core";
import {
  IconArrowDown,
  IconArrowsMaximize,
  IconBrandGithub,
  IconDeviceDesktop,
  IconPlayerPauseFilled,
  IconPlayerPlayFilled,
} from "@tabler/icons-react";
import { useRef, useState } from "react";

import { AUTHOR_LINKEDIN_URL, AUTHOR_NAME, BASE_URL, INSTALL_URL, REPO_URL } from "../config";
import { ClaudeIcon } from "./ClaudeIcon";
import "./MobileLanding.css";

// File lives at plugin/dashboard/public/dashboard-demo.mp4 — Vite copies it
// into the build root, then `make demo` rsyncs it to docs/ for GitHub Pages.
const PRODUCT_VIDEO_URL = `${BASE_URL}dashboard-demo.mp4`;

export function MobileLanding() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPaused, setIsPaused] = useState(false);

  const togglePlay = () => {
    const el = videoRef.current;
    if (!el) return;
    if (el.paused) {
      void el.play().catch(() => {});
    } else {
      el.pause();
    }
  };

  // Mobile Safari needs webkitEnterFullscreen() on the video element itself;
  // the standard Fullscreen API on iOS only works on a few elements and
  // doesn't include video. Fall back to standard requestFullscreen elsewhere.
  const handleFullscreen = () => {
    const el = videoRef.current;
    if (!el) return;
    const ios = el as HTMLVideoElement & { webkitEnterFullscreen?: () => void };
    if (ios.webkitEnterFullscreen) {
      ios.webkitEnterFullscreen();
    } else if (el.requestFullscreen) {
      void el.requestFullscreen();
    }
  };

  return (
    <Box className="mobile-landing">
      <Container size="sm" px="md" pt="xl" pb={112}>
        <Stack gap={8}>
          <Title order={1} fw={600} fz={34} style={{ lineHeight: 1.15 }}>
            pm-job-search
          </Title>
          <Text size="md" c="dimmed" style={{ lineHeight: 1.5 }}>
            A <ClaudeIcon size={14} />Claude Code plugin that runs your senior-PM job search
            end-to-end from the terminal.
          </Text>
        </Stack>

        <Box
          mt="xl"
          p="md"
          style={{
            background: "var(--mantine-color-dark-6)",
            borderRadius: 10,
          }}
        >
          <Group gap="sm" align="flex-start" wrap="nowrap">
            <IconDeviceDesktop
              size={20}
              style={{ flexShrink: 0, marginTop: 2, color: "var(--mantine-color-dimmed)" }}
            />
            <Box>
              <Text size="sm" fw={600} mb={4}>
                Built for desktop
              </Text>
              <Text size="sm" c="dimmed" style={{ lineHeight: 1.5 }} mb={6}>
                Claude Code is a terminal app — open this page on a laptop to install the plugin and
                try the live dashboard demo.
              </Text>
              <Anchor
                href="#dashboard-video"
                size="sm"
                fw={500}
                style={{ display: "inline-flex", alignItems: "center", gap: 4 }}
              >
                See it in motion
                <IconArrowDown size={14} />
              </Anchor>
            </Box>
          </Group>
        </Box>

        <Stack gap={32} mt={40}>
          <Section title="What the plugin does">
            <Text size="sm" mb={10} style={{ lineHeight: 1.6 }}>
              The work happens through commands in Claude Code:
            </Text>
            <List size="sm" spacing={8} styles={{ itemWrapper: { lineHeight: 1.5 } }}>
              <List.Item>
                <strong>Discover & score</strong> — weekly sweep of target companies plus one-off
                postings scored against your own rubric.
              </List.Item>
              <List.Item>
                <strong>Apply</strong> — tailors your CV per role; every claim traces back to your
                master CV or your own answers.
              </List.Item>
              <List.Item>
                <strong>Interview prep</strong> — adapts stories from your STAR-story bank for each
                round.
              </List.Item>
              <List.Item>
                <strong>Evaluate the offer</strong> — checks comp, anti-goals, and the senior-PM
                archetype.
              </List.Item>
              <List.Item>
                <strong>Honest career coach</strong> — pushes back when the search itself isn't
                working.
              </List.Item>
            </List>
          </Section>

          <Section title="What this dashboard is">
            <Text size="sm" mb={10} style={{ lineHeight: 1.6 }}>
              An optional visual layer on top of the plugin. You open it from inside Claude Code
              with <code>/pm-job-search:dashboard</code> — it launches in your browser and reads
              the same files the plugin's other commands work with.
            </Text>
            <Text size="sm" style={{ lineHeight: 1.6 }}>
              The terminal is great for thinking-and-writing work. The dashboard is for the moments
              in between:
            </Text>
            <List size="sm" spacing={6} mt={8} styles={{ itemWrapper: { lineHeight: 1.5 } }}>
              <List.Item>
                Scanning the whole pipeline at a glance, especially with many open roles.
              </List.Item>
              <List.Item>
                Bumping a status after a recruiter call, or jotting a note between meetings.
              </List.Item>
              <List.Item>
                Reading a research brief, prep doc, or interview debrief without opening files.
              </List.Item>
            </List>
          </Section>

          <Section title="Yours, on your machine">
            <Text size="sm" style={{ lineHeight: 1.6 }}>
              Everything lives on your laptop — your pipeline, your notes, your interview prep.
              Nothing is sent to a server, nothing is shared with anyone, nothing leaves until you
              choose.
            </Text>
          </Section>

          <Stack gap={10} id="dashboard-video" style={{ scrollMarginTop: 16 }}>
            <Text
              fz="xs"
              fw={600}
              tt="uppercase"
              c="dimmed"
              style={{ letterSpacing: "0.04em" }}
            >
              The dashboard in motion
            </Text>
            <Box
              className={`mobile-landing-video-wrapper ${isPaused ? "is-paused" : "is-playing"}`}
              onClick={togglePlay}
              role="button"
              tabIndex={0}
              aria-label={isPaused ? "Play video" : "Pause video"}
            >
              <video
                ref={videoRef}
                className="mobile-landing-video"
                src={PRODUCT_VIDEO_URL}
                autoPlay
                muted
                loop
                playsInline
                preload="auto"
                onPlay={() => setIsPaused(false)}
                onPause={() => setIsPaused(true)}
              >
                <Anchor href={PRODUCT_VIDEO_URL} target="_blank" rel="noopener noreferrer">
                  Watch on GitHub
                </Anchor>
              </video>
              <Box className="mobile-landing-video-overlay">
                <Box className="mobile-landing-video-overlay-icon">
                  {isPaused ? (
                    <IconPlayerPlayFilled size={28} />
                  ) : (
                    <IconPlayerPauseFilled size={28} />
                  )}
                </Box>
              </Box>
              <ActionIcon
                variant="filled"
                color="dark"
                size="lg"
                radius="md"
                className="mobile-landing-fullscreen-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  handleFullscreen();
                }}
                aria-label="Open video fullscreen"
              >
                <IconArrowsMaximize size={18} />
              </ActionIcon>
            </Box>
          </Stack>

          <Section title="Built by">
            <Anchor
              href={AUTHOR_LINKEDIN_URL}
              target="_blank"
              rel="noopener noreferrer"
              fw={500}
              size="sm"
            >
              {AUTHOR_NAME}
            </Anchor>
            <Text size="sm" c="dimmed" mt={4}>
              © {new Date().getFullYear()}
            </Text>
          </Section>
        </Stack>
      </Container>

      <Box className="mobile-landing-footer">
        <Container size="sm" px="md">
          <Group gap="sm" wrap="nowrap" justify="center">
            <Anchor
              href={INSTALL_URL}
              target="_blank"
              rel="noopener noreferrer"
              underline="never"
              style={{ flex: 1 }}
            >
              <Button variant="default" size="md" fullWidth>
                How to install
              </Button>
            </Anchor>
            <Anchor
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              underline="never"
              style={{ flex: 1 }}
            >
              <Button size="md" fullWidth leftSection={<IconBrandGithub size={16} />}>
                GitHub
              </Button>
            </Anchor>
          </Group>
        </Container>
      </Box>
    </Box>
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
        mb={10}
        style={{ letterSpacing: "0.04em" }}
      >
        {title}
      </Text>
      {children}
    </div>
  );
}
