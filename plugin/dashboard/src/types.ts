export type Status =
  | "new"
  | "to_apply"
  | "applied"
  | "interviewing"
  | "offer"
  | "rejected"
  | "not_interested";

export type Tier = "P0" | "P1" | "P2" | "P3";

export interface Position {
  company: string;
  position: string;
  position_slug: string;
  tier: Tier | string;
  status: Status | string;
  folder_path: string;
  is_multi_role: boolean;
  has_notes: boolean;
  score?: string;
  link?: string;
  date_added?: string;
  date_applied?: string;
  last_inbound?: string;
  monitoring?: string;
}

export interface WeeklyTargets {
  [key: string]: number;
}

export interface Strategy {
  target_offer_date?: string;
  weekly_targets: WeeklyTargets;
}

export interface DailyBrief {
  date: string;
  markdown: string;
}

export interface WeeklyProgress {
  warm_outreach: number;
  applications: number;
  window_days: number;
}

export interface DashboardState {
  companies: Position[];
  strategy: Strategy;
  weekly_progress: WeeklyProgress;
  latest_brief: DailyBrief | null;
  userdata_root: string;
}
