// Minimal Postiz REST client — schedules one post across multiple integrations.
// API surface mirrors the public docs at https://docs.postiz.com.

const baseUrl = (): string => {
  const v = process.env.POSTIZ_BASE_URL;
  if (!v) throw new Error("POSTIZ_BASE_URL not set");
  return v.replace(/\/$/, "");
};

const apiKey = (): string => {
  const v = process.env.POSTIZ_API_KEY;
  if (!v) throw new Error("POSTIZ_API_KEY not set");
  return v;
};

export interface IntegrationSummary {
  id: string;
  providerIdentifier: "tiktok" | "instagram" | "youtube" | string;
  name: string;
}

export interface ScheduleArgs {
  videoUrl: string;
  caption: string;
  scheduledAt: Date;
  integrationIds: string[];
  perChannel?: Record<string, unknown>; // platform-specific overrides
}

async function call<T>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await fetch(`${baseUrl()}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${apiKey()}`,
      "Content-Type": "application/json",
      ...(init.headers ?? {}),
    },
  });
  if (!res.ok) throw new Error(`Postiz ${res.status} ${await res.text()}`);
  return res.json() as Promise<T>;
}

export async function listIntegrations(): Promise<IntegrationSummary[]> {
  return call<IntegrationSummary[]>("/public/v1/integrations");
}

export async function schedulePost(args: ScheduleArgs): Promise<{ id: string }> {
  return call<{ id: string }>("/public/v1/posts", {
    method: "POST",
    body: JSON.stringify({
      type: "schedule",
      date: args.scheduledAt.toISOString(),
      posts: args.integrationIds.map((id) => ({
        integration: { id },
        value: [{ content: args.caption, image: [{ path: args.videoUrl }] }],
        settings: args.perChannel?.[id] ?? {},
      })),
    }),
  });
}
