# 08. セットアップ手順 (Postiz + Cloudflare R2 + GitHub Secrets)

このドキュメントは「動画自動投稿パイプライン」を稼働させるための初期セットアップ手順。1 回だけ実行する設定作業をまとめる。出先のスマホ・タブレットからでも進められるよう、すべてブラウザ操作で完結する構成にしてある。

所要時間: 30〜60 分。順番に上から実行。

---

## 0. 前提

- GitHub アカウント (Reel-Generator リポのオーナー)
- クレジットカード (Cloudflare R2 と Railway 課金登録 — 無料枠で運用予定)
- TikTok / Instagram (Business アカウント or Creator アカウント、要 Facebook Page リンク) / YouTube チャンネル
- メールアドレス × 3 (各サービスのアカウント用、既存可)

---

## 1. Cloudflare R2 (動画ストレージ)

R2 は完成動画を置く保管庫。GitHub Actions が動画をアップロード、Postiz が公開 URL から動画を取り込む。Egress 課金がないので動画ホスティングに最適。

### 1.1 Cloudflare アカウント作成

1. https://dash.cloudflare.com/sign-up にアクセス → メール + パスワードで登録
2. メール認証
3. ダッシュボードに入る

### 1.2 R2 を有効化

1. 左サイドバー → **R2 Object Storage**
2. **Purchase R2** をクリック → 支払い情報を登録
   - 無料枠: 月 10 GB ストレージ、Class A ops 1M、Class B ops 10M、**egress 完全無料**
   - 本パイプラインは月 10 GB 以内で収まる想定 (1 本 ~20 MB × 月 30 本 = 600 MB)

### 1.3 バケット作成

1. **Create bucket** をクリック
2. Bucket name: `reel-generator-final` (グローバルでユニーク、必要なら suffix を追加)
3. Location: **Automatic** (推奨)
4. Default storage class: **Standard**
5. **Create bucket**

### 1.4 パブリック公開設定

Postiz から動画を取りに行くため、バケットに公開 URL を持たせる。

1. 作成したバケットを開く → **Settings** タブ
2. **Public access** → **R2.dev subdomain** → **Allow Access**
3. 表示される `https://pub-<hash>.r2.dev` をメモ (`R2_PUBLIC_BASE_URL`)

### 1.5 API トークン作成

GitHub Actions からのアップロード用。

1. 左サイドバー → **R2** → **Manage R2 API Tokens**
2. **Create API Token**
3. Token name: `reel-generator-ci`
4. Permissions: **Object Read & Write**
5. Specify bucket(s): 上記バケットのみ選択
6. TTL: なし (long-lived)
7. **Create API Token**
8. 以下 3 つを安全な場所にコピー (R2 画面を閉じると Secret Access Key は再表示不可):
   - **Access Key ID** → `R2_ACCESS_KEY_ID`
   - **Secret Access Key** → `R2_SECRET_ACCESS_KEY`
   - **Endpoint** (Account ID 入り URL) → `R2_ENDPOINT`

---

## 2. Postiz セルフホスト (Railway)

Postiz は予約投稿の中枢。Railway にデプロイすると Web UI + REST API + MCP サーバーが立ち上がる。

### 2.1 Railway アカウント作成

1. https://railway.app → **Login with GitHub**
2. GitHub 認可
3. プラン: Hobby ($5/月クレジット付き、最初はこれで足りる)

### 2.2 Postiz デプロイ

公式テンプレを使う:

1. https://railway.com/deploy/postiz を開く
2. **Deploy Now**
3. デプロイ先プロジェクト名: `reel-generator-postiz`
4. 環境変数は **デフォルトのまま** で OK (テンプレが自動で生成)
5. 5-10 分待つと PostgreSQL + Redis + Postiz が起動

### 2.3 Postiz の公開 URL を取得

1. デプロイ完了後、Postiz サービスをクリック → **Settings** → **Networking**
2. **Generate Domain** で Railway 生成ドメインを発行 → URL をコピー (例: `https://reel-generator-postiz-production.up.railway.app`)
3. メモ → `POSTIZ_BASE_URL`

### 2.4 初回ログイン

1. 上記 URL をブラウザで開く
2. 管理者アカウント作成 (メール + パスワード)
3. ダッシュボードに入る

### 2.5 SNS チャネル連携

各プラットフォームを Postiz に OAuth 接続する。Postiz が TikTok の UI 要件 (ユーザー名表示 / プライバシー選択) を満たしているので、自前で TikTok 審査を通す必要はない。

ダッシュボード → **Launches** or **Settings** → **Channels** → **Add Channel** から:

#### TikTok
- TikTok ログイン → Postiz への投稿権限を許可
- Postiz のテナント設定で TikTok の credentials を Self-Provided とする選択肢が出る場合、開発用は Postiz Demo で開始可、本番運用前に TikTok for Developers で自分のアプリを作って差し替え推奨

#### Instagram (Reels)
- **必須**: Instagram Business アカウントに切替済、Facebook Page にリンク済
- Postiz の Add Channel → Instagram → Facebook ログイン → 対象 Business アカウントを選択

#### YouTube (Shorts)
- Google ログイン → 対象 YouTube チャンネルを選択 → YouTube アップロード権限を許可

### 2.6 API キー発行

GitHub Actions からの公開予約投稿用。

1. ダッシュボード → **Settings** → **API Keys** (or **Developer** → **API Keys**)
2. **Create API Key** → name: `github-actions-ci`、scope: posts:write、保存
3. キーをコピー → `POSTIZ_API_KEY`
4. 同じ画面の **Organization ID** もメモ → `POSTIZ_ORG_ID` (組織必須の API がある場合)

### 2.7 試験投稿 (手動)

API パイプラインを通す前に手動 1 本通す。

1. ダッシュボードで **New Post** → Sample テキスト + Sample 画像
2. 3 チャネル全て選択 → 5 分後に予約 → 保存
3. 5 分後、各プラットフォームに投稿が出ているか確認
4. 確認できたら削除して OK

---

## 3. GitHub Repository Secrets

GitHub Actions から各 API を叩けるよう、シークレットを登録。

1. Reel-Generator リポジトリの GitHub ページ → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** で以下を 1 件ずつ追加:

| 名前 | 値 | 取得場所 |
| ---- | -- | -------- |
| `HIGGSFIELD_API_KEY` | (Higgsfield のキー) | https://higgsfield.ai → Account → API |
| `R2_ACCESS_KEY_ID` | 上記 1.5 でコピー | Cloudflare R2 token |
| `R2_SECRET_ACCESS_KEY` | 上記 1.5 でコピー | 同上 |
| `R2_ENDPOINT` | 上記 1.5 でコピー | 同上 |
| `R2_BUCKET` | `reel-generator-final` | 1.3 で決めた名前 |
| `R2_PUBLIC_BASE_URL` | 上記 1.4 でコピー | R2 public subdomain |
| `POSTIZ_BASE_URL` | 上記 2.3 でコピー | Railway domain |
| `POSTIZ_API_KEY` | 上記 2.6 でコピー | Postiz Settings |
| `POSTIZ_ORG_ID` | 上記 2.6 でコピー (任意) | 同上 |
| `OPENAI_API_KEY` | 任意 (whisper 用) | OpenAI Platform |
| `SLACK_WEBHOOK_URL` | 任意 (通知用) | Slack App |

---

## 4. 動作確認 (Phase 7-γ クロージング)

### 4.1 verify-setup workflow を手動実行
リポの **Actions** タブ → **verify-setup** → **Run workflow** → main → 緑になれば全シークレット通電完了。
このワークフローは Higgsfield 残高を読むだけ・R2 に小さなテキストファイルを 1 回 PUT/GET/DELETE するだけ・Postiz の integrations を一覧するだけ で、課金もなければ実投稿もしない。

失敗パターンと対処:
- `missing required env vars` → リポ Secrets を見直し
- `r2 public read failed` → 1.4 の R2.dev subdomain が allow access になっているか確認
- `postiz 401` → API キーの scope を確認、ローテーションして登録し直し

### 4.2 1 ネタを通す
verify が緑になったら **generate** workflow を手動実行 (slug = `loud-snack` 等) → 自動 PR が立ち、`content/ready/<slug>.json` に R2 公開 URL が記録される → マージで **publish** workflow が次の cron で予約投稿に流す。
最初は publish の `dry_run` を true で 1 回回し、ログに「投稿予定」が出るのを確認してから false に切り替える。

---

## 5. トラブルシューティング

| 症状 | 対処 |
| ---- | ---- |
| R2 へのアップロードが 403 | API トークンの bucket scope を確認、`R2_ENDPOINT` に account id が入っているか確認 |
| Postiz の TikTok 投稿が pending のまま | Postiz の TikTok integration を `Open` (Self-Hosted) ではなく `Postiz Demo` で繋いだか確認 |
| Instagram 投稿が拒否される | Business アカウント + FB Page リンクを再確認。9:16 / 5-90s / H.264 / mp4 のみ |
| Postiz が落ちる | Railway の Service → Logs を確認。Redis/Postgres の接続文字列を再確認 |
| Higgsfield API が credits 切れ | Higgsfield 側で credit top-up |

---

## 6. このセットアップで動くもの

- ✅ GitHub Actions 上で Higgsfield → R2 → Postiz の自動パイプラインが回る
- ✅ スマホから GitHub の Web UI で手動再実行・yaml 編集が可能
- ✅ 動画は R2 に保管 (egress 無料、月 10GB 内で $0)
- ✅ Postiz で 3 チャネル同時予約 (TikTok 審査不要)
- ✅ MCP 経由で Claude Code から直接「明日 19 時に投げて」と指示も可能

次のフェーズ (`pipelines/` 実装) は `docs/07-automation-architecture.md` を参照。