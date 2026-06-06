// Drains content/ready/*.json into Postiz scheduled posts.
//
// Run via: `npm run schedule` (or `npm run publish:dry` for a no-op preview).
// Moves successfully scheduled items into content/archive/.

import { readFile, readdir, rename, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import yaml from "yaml";
import { z } from "zod";
import { listIntegrations, schedulePost } from "./postiz.ts";

const ROOT = path.resolve(import.meta.dirname, "../..");
const READY = path.join(ROOT, "content/ready");
const ARCHIVE = path.join(ROOT, "content/archive");
const CHANNELS_YAML = path.join(ROOT, "config/channels.yaml");
const DRY_RUN = process.env.DRY_RUN === "true";

const ReadyItem = z.object({
  slug: z.string(),
  series: z.string(),
  title: z.string(),
  hook: z.string(),
  video_url: z.string().url(),
  series_cfg: z.object({ caption_template: z.string() }).passthrough(),
});

interface ChannelCfg {
  enabled: boolean;
  offset_hours: number;
  hashtags: string[];
}

function captionFor(item: z.infer<typeof ReadyItem>, channel: string, cfg: ChannelCfg): string {
  const base = item.series_cfg.caption_template.replace("{hook}", item.hook);
  const tags = cfg.hashtags.map((h) => `#${h}`).join(" ");
  return `${base}\n\n${tags}`.trim();
}

async function main() {
  if (!existsSync(READY)) {
    console.log("no content/ready/ — nothing to do");
    return;
  }
  const channels = yaml.parse(await readFile(CHANNELS_YAML, "utf8")) as Record<string, ChannelCfg>;
  const integrations = DRY_RUN ? [] : await listIntegrations();
  const integrationByProvider = new Map(integrations.map((i) => [i.providerIdentifier, i.id]));

  const files = (await readdir(READY)).filter((f) => f.endsWith(".json"));
  if (!files.length) {
    console.log("no ready items");
    return;
  }

  for (const file of files) {
    const item = ReadyItem.parse(JSON.parse(await readFile(path.join(READY, file), "utf8")));
    const now = Date.now();
    for (const [channel, cfg] of Object.entries(channels)) {
      if (!cfg.enabled) continue;
      const integrationId = integrationByProvider.get(channel);
      if (!integrationId && !DRY_RUN) {
        console.warn(`skipping ${channel}: no integration connected in Postiz`);
        continue;
      }
      const scheduledAt = new Date(now + cfg.offset_hours * 3600 * 1000);
      const caption = captionFor(item, channel, cfg);
      console.log(`[${DRY_RUN ? "DRY" : "POST"}] ${item.slug} → ${channel} @ ${scheduledAt.toISOString()}`);
      if (DRY_RUN) continue;
      await schedulePost({
        videoUrl: item.video_url,
        caption,
        scheduledAt,
        integrationIds: [integrationId!],
      });
    }
    if (!DRY_RUN) {
      const archived = path.join(ARCHIVE, file);
      await rename(path.join(READY, file), archived);
      // Append a small posting log next to the archive item.
      const log = { posted_at: new Date().toISOString(), ...item };
      await writeFile(archived.replace(/\.json$/, ".posted.json"), JSON.stringify(log, null, 2));
    }
  }
}

await main();
