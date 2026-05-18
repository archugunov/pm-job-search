import { Alert, Button, Modal, Select, Stack, TextInput } from "@mantine/core";
import { useState } from "react";

import { ApiError, postCompany } from "../api";

const STATUS_OPTIONS = [
  "discovered",
  "applied",
  "interviewing",
];

const TIER_OPTIONS = ["P0", "P1", "P2", "P3"];

interface Props {
  opened: boolean;
  onClose: () => void;
  onCreated: () => void;
}

export function NewCompanyModal({ opened, onClose, onCreated }: Props) {
  const [company, setCompany] = useState("");
  const [position, setPosition] = useState("");
  const [tier, setTier] = useState<string>("P1");
  const [link, setLink] = useState("");
  const [status, setStatus] = useState<string>("discovered");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const reset = () => {
    setCompany("");
    setPosition("");
    setTier("P1");
    setLink("");
    setStatus("discovered");
    setError(null);
  };

  const submit = async () => {
    setError(null);
    if (!company.trim() || !position.trim() || !link.trim()) {
      setError("Company, position, and link are required.");
      return;
    }
    setSaving(true);
    try {
      await postCompany({ company, position, tier, link, status });
      reset();
      onCreated();
      onClose();
    } catch (e) {
      if (e instanceof ApiError && e.status === 409) {
        setError(e.message);
      } else {
        setError(e instanceof Error ? e.message : "Failed to create company");
      }
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal opened={opened} onClose={onClose} title="Add company" centered>
      <Stack>
        <TextInput label="Company" value={company} onChange={(e) => setCompany(e.currentTarget.value)} required />
        <TextInput label="Position" value={position} onChange={(e) => setPosition(e.currentTarget.value)} required />
        <Select label="Tier" data={TIER_OPTIONS} value={tier} onChange={(v) => v && setTier(v)} />
        <TextInput label="Link" value={link} onChange={(e) => setLink(e.currentTarget.value)} required />
        <Select label="Status" data={STATUS_OPTIONS} value={status} onChange={(v) => v && setStatus(v)} />
        {error && <Alert color="red">{error}</Alert>}
        <Button loading={saving} onClick={submit}>Create</Button>
      </Stack>
    </Modal>
  );
}
