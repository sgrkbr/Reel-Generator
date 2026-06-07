# 09. チャネル鞍替え設定 (TikTok / Instagram / YouTube)

既存 3 チャネルを **Couple Things** ブランドに切り替えるための完全チェックリスト。
各セクションは「**そのプラットフォームの設定画面に存在する全項目**」 → 推奨値の順。

---

## ブランド定義 (3 チャネル共通)

| 項目 | 値 |
| ---- | -- |
| ブランド名 / Display name | `Couple Things` |
| タグライン (一行) | `Animated everyday couple moments. New short every couple of days.` |
| ハンドル (確定) | **`couplethings_daily`** ✅ |
| 確定 URL | TikTok: https://www.tiktok.com/@couplethings_daily<br>Instagram: https://www.instagram.com/couplethings_daily/<br>YouTube: https://www.youtube.com/@couplethings_daily |
| ニッチ | Couple-life observational humor, 2D animated short videos |
| ターゲット言語 | 英語 (グローバル) |
| トーン | Self-deprecating + dry + warm |
| プライマリ CTA | Follow for daily couple moments |
| 外部リンク (1 個まとめ) | Linktree / Beacons / Bento (まとめページを作って 3 チャネル共通で貼る — Postiz が用意するページでも可) |
| 連絡用メール | `couplethings.contact@gmail.com` (新規作成推奨、既存可) |
| 国 / 言語設定 | United States / English (グローバル配信狙い) |

> **改名タイミング注**: TikTok の `username` 変更は 30 日に 1 回まで。Instagram の `username` は変更しても **約 14 日間は旧 username の URL が予約される** ので、安全に取り直す前提なら影響少。YouTube の `@handle` は **14 日間に 2 回まで** 変更可。

---

## 必要画像素材一覧

| ファイル | サイズ (px) | 用途 | 配置 |
| -------- | ----------- | ---- | ---- |
| `icon.png` | **1080×1080** 推奨 (最低 320×320) | 3 チャネル共通プロフィール画像 (円形クロップ) | TikTok / IG / YouTube |
| `youtube-banner.png` | **2560×1440** (safe area 1546×423 中央) | YouTube チャンネルアート | YouTube のみ |
| `youtube-watermark.png` | **150×150** 透過 PNG | 動画再生中右下に表示 | YouTube のみ |
| (任意) IG ハイライト カバー × 5 | 1080×1080 | 1人語り / カップル / 旅 / 仕事 / Behind | IG のみ |

生成済アセット URL は本ドキュメント末尾を参照。

---

## TikTok 設定 — 既存: [`@ai.trendnews`](https://www.tiktok.com/@ai.trendnews)

### Profile (Edit Profile から)

| フィールド | 文字制限 | 推奨値 |
| ---------- | -------- | ------ |
| Profile photo | 1:1 | `icon.png` |
| Profile video (optional) | 9:16 / 1080×1920 / 6s 以内 | ピンク色のループ短尺 (後で) — 当面なし |
| Name (Display name) | 30 chars | `Couple Things` |
| Username (Handle) | 4-24 chars, `a-z0-9._` | `couplethings` (取れなければ `couplethings.daily`) |
| Pronouns | — | 空 (中性ブランド) |
| Bio | **80 chars** | `Animated couple moments. New short every couple of days 💞` (66) |
| Add link in bio | 100 chars | Linktree 等 1 つ |
| Add Instagram | — | IG ハンドル連携 |
| Add YouTube | — | YouTube ハンドル連携 |

### Account 系設定

- **Switch to Business / Creator アカウント**: Creator 推奨 (Business は CTA ボタン使えるが楽曲制約あり)
- Category: `Personal blog` / `Entertainment`
- Contact email: 上記共通アドレス
- Privacy: Public

### 既存コンテンツ
- 旧 `@ai.trendnews` の AI ニュース動画は **アーカイブ非公開**にしてから改名 (履歴は残るがアクセス不可)
- アーカイブ前にプロフィールへ「**Channel relaunching as Couple Things — old AI news content archived**」と 24h 投稿しておくと、follower の不審離脱を減らせる

---

## Instagram 設定 — 既存: [`@ken_tanaka_ai`](https://www.instagram.com/ken_tanaka_ai/?hl=en)

### Profile (Edit Profile から)

| フィールド | 文字制限 | 推奨値 |
| ---------- | -------- | ------ |
| Profile photo | 1:1 | `icon.png` |
| Name (Display name) | 30 chars | `Couple Things` |
| Username (Handle) | 30 chars, `a-z0-9._` | TikTok と同じ |
| Pronouns | — | 空 |
| Bio | **150 chars** | `Animated everyday couple moments 💞\nNew shorts every couple of days\nReels • Shorts • TikTok` (101) |
| Links | 最大 5 個 (Edit links 経由) | 1: Linktree / 2: TikTok / 3: YouTube |
| Gender | — | 空 |
| Category (Business/Creator のみ) | — | `Entertainment` or `Creator/Personal Blog` |
| Contact options (Business のみ) | — | 上記共通メール |
| Action button (Business のみ) | — | なし |

### Account 系設定
- **Switch to Professional account → Creator** (Reels API publish に **後から Business が必要**だが、いまは Creator で十分。Reels 自動投稿に切替時に Business 化)
- Linked accounts: Facebook Page 連携 (将来の Graph API 用)
- Branded content: OFF
- Private account: OFF

### 既存コンテンツ
- 旧 `@ken_tanaka_ai` の投稿は **アーカイブ (Archive Post)** で非公開化、削除はしない (後で復元可能性のため)
- Highlights は一旦全削除、新ブランドのカバー画像で作り直し (任意フェーズ)

---

## YouTube 設定 — 既存: [`@leadersnote`](https://www.youtube.com/@leadersnote)

### Basic info

| フィールド | 文字制限 | 推奨値 |
| ---------- | -------- | ------ |
| Channel name | 100 chars | `Couple Things` |
| Handle | 3-30 chars, `a-z0-9._-` 一意 | `@couplethings` (取れなければ `@couplethings_daily`) |
| Description | **1000 chars** | 下記テンプレ |
| Default language | — | English |
| Country | — | United States |

**Description テンプレ** (824 chars):
```
Couple Things is an animated short-video series about everyday partner moments — the loud snack at 1:47 AM, the calendar invite you didn't agree to, the "fine" that meant absolutely not fine.

Wife + husband. Two characters. One apartment. Zero filters.

🎬 New animated short every couple of days
📱 Vertical 9:16 — best on mobile
💞 Built for couples who recognize themselves in the small stuff

Also on TikTok: @couplethings_daily
Also on Instagram: @couplethings_daily

Business: couplethings.contact@gmail.com
```

### Branding (Customization → Branding)

| 項目 | サイズ | アセット |
| ---- | ------ | -------- |
| Picture (channel icon) | 800×800 推奨 (98×98 min) | `icon.png` |
| Banner image | **2048×1152 min, 6 MB 以下** (2560×1440 推奨, safe area 1546×423) | `youtube-banner.png` |
| Video watermark | 150×150 推奨 (1 MB 以下、透過 PNG) | `youtube-watermark.png` (表示タイミング: Entire video) |

### Layout (Customization → Layout)

- Channel trailer (非登録者向け): 後で 1 本投稿してから設定
- Featured video (登録者向け): 最新作を自動表示する設定でも OK
- Featured sections:
  1. Shorts (auto)
  2. Popular videos
  3. (任意) Playlists by series (Couple Things / Inner Voice / Couple WFH)

### Basic info → Links

| 表示テキスト | URL |
| ------------ | --- |
| TikTok | `https://www.tiktok.com/@couplethings_daily` |
| Instagram | `https://www.instagram.com/couplethings_daily/` |
| Linktree | (Linktree URL — 任意) |

### Settings → Channel → Advanced settings

- Audience: `No, set this channel as not made for kids` (大人向けユーモア)
- Keywords (500 chars): `couple humor, couple things, animated couple, animated shorts, relationship humor, couple animation, daily couple, wife husband humor, couple comedy, couple skits, relatable couple, couple reels, couple shorts, animation, 2d animation, animated series, animated comedy, animated skit, animated story, cartoon, cartoon comedy, animated short film, indie animation, character animation, animation channel, animation studio, motion design, flat animation, daily animation`
- Country of audience: 制限なし

### Settings → Upload defaults

- Title: (各動画ごと)
- Description テンプレ (1 投稿あたり):
  ```
  {hook line}

  More Couple Things: https://youtube.com/@couplethings_daily
  TikTok: https://tiktok.com/@couplethings_daily
  Instagram: https://instagram.com/couplethings_daily

  #couplethings #couplehumor #animation #shorts
  ```
- Visibility: Public
- Category: `Entertainment`
- License: `Standard YouTube License`
- Comments: Allow all (Hold potentially inappropriate for review = ON)
- Show how many viewers like and dislike this video: ON

### 既存コンテンツ
- 旧 `@leadersnote` の動画は **Unlisted** に一括変更 (削除はしない)
- Playlist 群は非公開 (Private)
- Comments / Community posts は履歴として残す

---

## 共通アクション順序 (1 サイクルで終わらせる)

1. **(任意)** 新メールアドレス `couplethings.contact@gmail.com` を作る (or 既存メール流用)
2. Linktree / Beacons / Bento でリンクハブを作り、3 チャネル URL を投入 (URL を取得)
3. **YouTube**: 設定 → Customization → 画像 3 種・Description・Links を更新 → Handle 変更 → 旧動画 Unlisted 化
4. **Instagram**: Account type を Professional/Creator に → Edit profile で Name/Username/Bio/Photo を更新 → 旧投稿アーカイブ
5. **TikTok**: Edit profile で Photo/Name/Username/Bio を更新 → 旧動画 Private 化 (アーカイブ通知投稿を 24h 先に上げる)

所要 30-90 分 (画像差し替えと旧動画整理含む)。

---

## 生成済ブランドアセット (Higgsfield)

| アセット | Job ID | URL |
| -------- | ------ | --- |
| Icon (1:1) v2 | `7faabe94-d186-4889-9c25-f89fac9b7b26` | https://d8j0ntlcm91z4.cloudfront.net/user_3DHZDwYAr0mvwHad9r4Zby8yRNL/hf_20260607_074518_7faabe94-d186-4889-9c25-f89fac9b7b26.png |
| YouTube Banner (16:9) v3 | `8ece404d-5d1a-43fb-badc-b6d97520fb58` | https://d8j0ntlcm91z4.cloudfront.net/user_3DHZDwYAr0mvwHad9r4Zby8yRNL/hf_20260607_112421_8ece404d-5d1a-43fb-badc-b6d97520fb58.png |
| YouTube Watermark (1:1) v3 | `4ab60878-6a44-43df-9768-fc2b5d57d320` | https://d8j0ntlcm91z4.cloudfront.net/user_3DHZDwYAr0mvwHad9r4Zby8yRNL/hf_20260607_074718_4ab60878-6a44-43df-9768-fc2b5d57d320.png |
| _v1/v2 (archived)_ | _904b5e51 / 5d9daac7 / 8a0352e1 / c75532f3_ | (replaced by v2/v3 above) |

> URL は完成し次第このファイル末尾に追記。
> ダウンロード後リサイズが必要なら CapCut / Photoshop / Squoosh などで:
> - YouTube banner: 2560×1440 にアップスケール、jpeg 品質 85 で 6 MB 以下に。
> - Watermark: 150×150 に縮小、背景透過化 (Remove BG / Photoshop 透過処理)。

---

## 後で追加するもの (任意)

- IG Highlights カバー × 5 (Couple Things / Inner Voice / WFH / Travels / Behind)
- TikTok Profile video (6s ループ)
- YouTube Channel trailer (15-30s "what this channel is" の自己紹介ショート)
- Linktree カスタムテーマ (peach-cream パレットで合わせる)