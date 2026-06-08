# 10. 公式 API クレデンシャル申請手順

3 プラットフォームを GitHub Actions から直叩きするための「開発者アプリ申請 → クレデンシャル取得」一括手順。

---

## A. TikTok Content Posting API ⭐最優先 (リードタイム最長)

### 0. 申請前チェックリスト
| 必要なもの | 値 / 場所 |
| ---------- | --------- |
| TikTok アカウント (個人 or `@couplethings_daily`) | TikTok ログイン |
| Privacy Policy URL (Notion 公開) | (Notion `notion.site/...` の公開 URL) |
| Terms of Service URL (Notion 公開) | (同上) |
| App icon | `icon.png` (256×256 PNG 推奨) — Higgsfield 生成済を Squoosh で 256 にリサイズ |
| Web URL (アプリの主たる URL) | `https://linktr.ee/couplethings_daily` |
| Demo video (1-3 分) | 後で録画 (Sandbox で動かしてから OBS / Loom で OK) |
| アプリ用ロゴ正方形 | icon.png 流用 |

### 1. アカウント登録
1. https://developers.tiktok.com/ → 右上 **Log in** → TikTok ログイン
2. 初回はメール認証 + 利用規約同意 → 個人 or 組織情報を簡単に入力 (個人選択で OK)
3. 開発者ダッシュボードに着く

### 2. アプリ作成
1. 上部メニュー **Manage apps** → 右上 **Connect an app**
2. **App information** タブで以下入力:

   | フィールド | 入力値 |
   | ---------- | ------ |
   | App icon | `icon.png` (アップロード) |
   | App name | `Couple Things Publisher` |
   | App description | `Internal publishing tool that uploads animated couple-content short videos to the Couple Things TikTok channel (@couplethings_daily). The app authenticates the channel owner via TikTok Login Kit and uses the Content Posting API to publish 9:16 vertical animated shorts on a scheduled cadence.` (200-300 chars が安全) |
   | Category | `Entertainment` |
   | Web/Desktop URL | `https://linktr.ee/couplethings_daily` |
   | Terms of Service URL | (Notion 公開 URL — Terms) |
   | Privacy Policy URL | (Notion 公開 URL — Privacy) |
   | Platform | `Web` を選択 |

3. **Save** → アプリ作成完了。**Client Key** と **Client Secret** が発行されるのでメモ:
   - → GitHub Secret 名: `TIKTOK_CLIENT_KEY` / `TIKTOK_CLIENT_SECRET`

### 3. Products を追加
左サイドバー **Products** → **Add products**:
- **Login Kit** を追加
- **Content Posting API** を追加

### 4. Login Kit の設定
1. **Login Kit** タブを開く
2. **Scopes**: 以下にチェック
   - `user.info.basic` (必須)
   - `video.publish` (公開投稿に必須、audit 対象)
   - `video.upload` (Sandbox 検証に必須)
3. **Redirect URI** (HTTPS 必須):
   - 初期暫定: `https://linktr.ee/couplethings_daily`
   - 本番運用: GitHub Pages に空ページを 1 枚デプロイして使う (例: `https://<gh-user>.github.io/reel-generator/tiktok-callback`) — これは `docs/10` で後述
4. **Save**

### 5. Content Posting API の設定
1. **Content Posting API** タブを開く
2. **Direct Post mode** を選ぶ (Inbox mode は下書きに入るだけで自動化に不向き)
3. **Required scopes** (自動チェック): `video.publish`
4. **Save**

### 6. Sandbox 検証 (審査前にここで疎通テスト)
1. 左サイドバー **Sandbox** → **Add target users**
2. **TikTok username** に `couplethings_daily` (本番 SNS アカウント) を追加 — Sandbox 中はこのアカウントにだけ private 投稿可能
3. パイプライン側からアクセストークン取得 → API テスト投稿 → TikTok アプリで private 投稿として確認できれば疎通 OK

### 7. Production 審査申請
Sandbox 疎通が取れたら本番審査に出す:
1. 左サイドバー **App review** → **Submit for review**
2. **Audit submission form** に以下を入力:

   | フィールド | 入力値 |
   | ---------- | ------ |
   | Production scopes 要求 | `user.info.basic`, `video.publish`, `video.upload` |
   | Use case description | `Couple Things is an animated short-video brand publishing original 2D animated couple-life skits across TikTok, Instagram Reels, and YouTube Shorts. This internal publishing tool authenticates the brand's own TikTok account once via Login Kit, then uses the Content Posting API to upload pre-rendered MP4 reels on a publishing schedule managed by the brand team. No user-generated content is processed; every video is owned by the brand. The tool reduces manual upload effort and keeps a consistent posting cadence.` |
   | Demo video | 1-3 分の画面録画 (下記参照) |
   | Sample TikTok posts | 既存 reel URL を 1-2 個 (Sandbox 投稿の private URL でも可、または事前に手動で 1 本上げて URL を貼る) |

3. **Demo video の中身** (重要、ここで落ちると差し戻し): 以下を順番に映す:
   1. アプリ画面で「Connect TikTok」相当のボタンを押す
   2. TikTok の OAuth 画面が出てユーザが許可
   3. アプリに戻り、動画ファイル選択 + キャプション入力
   4. 「Publish」を押す
   5. TikTok アプリで該当投稿が表示される
   - OBS / Loom / QuickTime で録画 → YouTube に Unlisted で上げて URL を貼るのが最楽

4. **Submit** → 審査 1-2 週間。通れば Production mode に切り替わり、本番投稿が解禁される

### 8. 取得したいクレデンシャル一覧
申請完了後 (Sandbox 段階でもいい) に GitHub Secrets に登録するもの:

| Secret 名 | 値 | どこから |
| --------- | -- | -------- |
| `TIKTOK_CLIENT_KEY` | App 作成時に発行 | App information タブ |
| `TIKTOK_CLIENT_SECRET` | 〃 | 〃 |
| `TIKTOK_REFRESH_TOKEN` | OAuth フロー後に取得 (365 日有効) | 後述 |
| `TIKTOK_OPEN_ID` | OAuth 後にトークンと一緒に返る | 〃 |

### 9. Refresh token を 1 回だけ取る方法 (Sandbox 通った後)
GitHub Pages に空ページ 1 枚デプロイ → callback URL に登録 → ローカルから OAuth URL を踏む → code 返って来る → curl で refresh_token に交換 → GitHub Secrets に保存。詳細スクリプトは `scripts/tiktok_token_exchange.py` を別途用意 (Phase 7-γ で同梱)。

---

## B. Instagram Graph API (Meta for Developers)

(下書き) 後で詳細化。当面の段取り:
1. https://developers.facebook.com/ → My Apps → **Create App** → Use case: `Other` → Business app
2. アプリ名: `Couple Things Publisher` (TikTok と統一可)
3. Add products: `Instagram Graph API` + `Facebook Login for Business`
4. App Review で以下を申請 (Standard Access 必須):
   - `instagram_business_basic`
   - `instagram_business_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`
5. **Instagram → API setup with Instagram business login**:
   - Generate long-lived access token (60 日有効、refresh で延長可)
   - Instagram Business Account ID を取得
6. Secrets:
   - `META_APP_ID`
   - `META_APP_SECRET`
   - `IG_BUSINESS_ACCOUNT_ID`
   - `IG_LONG_LIVED_TOKEN`

審査は 1-7 日。事前に IG を Business 化 + FB Page 連携が必須 (`docs/09` 参照、ユーザは完了済)。

---

## C. YouTube Data API v3 (Google Cloud)

(下書き) 当面の段取り:
1. https://console.cloud.google.com → 新規プロジェクト `couple-things-publisher`
2. APIs & Services → **Enable APIs** → `YouTube Data API v3`
3. **OAuth consent screen** 設定:
   - User Type: `External`
   - App name: `Couple Things Publisher`
   - User support email: `couplethings.contact@gmail.com`
   - Developer email: 同上
   - App domain: `linktr.ee` (or 自社 domain 後で)
   - Privacy / Terms URL: Notion 公開 URL
   - Scopes: `https://www.googleapis.com/auth/youtube.upload`
   - **Test users** に自分の Google アカウントを追加 (本番審査前でも Test users なら使える)
4. **Credentials** → **Create Credentials** → `OAuth client ID`:
   - Type: `Web application`
   - Authorized redirect URI: 後で GitHub Pages のものに更新
5. クライアント JSON をダウンロード → secrets に保存
6. Secrets:
   - `YOUTUBE_CLIENT_ID`
   - `YOUTUBE_CLIENT_SECRET`
   - `YOUTUBE_REFRESH_TOKEN` (OAuth 後に取得)

審査は **Test users 100 名以内なら不要**、自分の YouTube チャンネルへの upload だけならそれで充分。本番審査出すと 1-3 週間。

---

## D. OAuth callback ホスティング (3 プラットフォーム共通)

3 つの API はいずれも HTTPS の Redirect URI を要求する。リッチなフロントは要らないので **GitHub Pages の空 HTML 1 枚**で OK。実装は `docs/10` 続編で記述、要点は:

- リポ内 `oauth-callback/index.html` を作成 → `code` パラメータを画面に表示するだけの HTML
- リポ設定で GitHub Pages を `main` branch / `/oauth-callback` ディレクトリで有効化
- 公開 URL `https://<gh-user>.github.io/Reel-Generator/oauth-callback/` を 3 プラットフォームの Redirect URI に設定
- ユーザは 1 度だけブラウザでアクセス → 表示された `code` を控える → ローカルスクリプトで `code → refresh_token` に交換 → GitHub Secret として保存

これで全自動化完成。
