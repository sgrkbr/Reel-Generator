# 07. 自動化アーキテクチャ (生成 + 投稿)

## ゴール

- **生成**: ネタ (Markdown) を入力すると Higgsfield で動画素材を生成、ffmpeg でアセンブル、字幕焼き込み、9:16 完成品まで出力
- **投稿**: 完成品を TikTok / Instagram Reels / YouTube Shorts へ Buffer 経由で予約投稿
- **運用**: 出先からスマホでも修正・実行できる、低コスト・低リスク

## 非ゴール (やらない)

- 完全無人運用 (品質ゲートは人がレビュー → 承認 → 投稿キューに入る半自動)
- ブラウザ自動操作 (BAN・ToS グレーのため除外)

## ランタイム選択: GitHub Actions

| 観点 | GitHub Actions | ローカル cron | Cloud Run |
| ---- | -------------- | ------------- | --------- |
| コスト | **無料枠 2000 分/月**で十分 | PC 起動依存 | 数百円/月〜 |
| 出先修正 | **github.com モバイル / iOS アプリで yaml 編集 & 手動実行可** | 不可 | デプロイ必須 |
| シークレット管理 | **リポジトリ Secrets** | .env 散在 | Secret Manager |
| API キー漏洩リスク | 低 (リポは private 前提) | 低 | 低 |
| デバッグ容易性 | ログがそのまま残る | 一番早い | やや面倒 |

→ **採用: GitHub Actions**。手元検証は CLI で同じスクリプトを叩く。

## 言語分担

- **Python (コア)**: Higgsfield API オーケストレーション、ffmpeg ラッパー、whisper による字幕タイミング、画像/動画アセット管理
- **TypeScript (薄いスクリプト)**: Buffer / TikTok / IG / YT API クライアント、設定ファイル変換、CLI エントリポイント
- **共通**: `config/` に YAML、`secrets/` は GH Secrets 経由

## ディレクトリ構成 (拡張案)

```
.
├── docs/                       # 既存
├── pipelines/
│   ├── generate/               # Python: 1ネタ → 完成動画
│   │   ├── orchestrator.py     # YAML を受けて全ショット生成
│   │   ├── higgsfield.py       # Higgsfield API ラッパー
│   │   ├── assemble.py         # ffmpeg でカット繋ぎ
│   │   ├── captions.py         # whisper → SRT → 焼き込み
│   │   └── virality_check.py   # 完成前にスコアリング
│   └── publish/                # TypeScript: 投稿
│       ├── buffer.ts           # Buffer API クライアント
│       ├── fallback_postiz.ts  # Buffer API が NG なら
│       └── schedule.ts         # 各チャネル時差展開
├── content/
│   ├── ideas/                  # 1.md = 1ネタ (フロントマター + スクリプト)
│   ├── ready/                  # レビュー済み投稿待ち
│   └── archive/                # 投稿済み
├── assets/                     # キャラ・背景の一貫性アセット
├── raw/                        # ショット生成中間物 (gitignore)
├── final/                      # 完成動画 (gitignore、外部ストレージに同期)
├── .github/workflows/
│   ├── generate.yml            # ideas/*.md push or 手動実行 → 生成
│   ├── publish.yml             # 1日1回 cron で ready/ をキューイング
│   └── nightly-research.yml    # 任意: ベンチアカ更新監視
├── config/
│   ├── series.yaml             # シリーズ定義
│   ├── channels.yaml           # 各チャネルのキャプション/タグ規則
│   └── characters.yaml         # キャラ一貫性アセット ID
└── scripts/
    ├── cli.py                  # ローカル実行用エントリ
    └── new-idea.sh             # テンプレ生成
```

## 大容量ファイル戦略

GitHub に動画は置かない (リポを軽く保つ + LFS 課金回避):
- **Higgsfield 生成物**: 一旦 Higgsfield 側に保持 → Python で URL ダウンロード → ffmpeg
- **完成動画 (`final/`)**: **Cloudflare R2** か **Backblaze B2** (どちらも egress 安い)
- メタデータと URL だけ git に commit

## 投稿経路: Postiz セルフホスト (本命) / 公式 API 直叩き (フォールバック)

### Phase 7-α 検証結果 (2026-06)

| 候補 | 結論 | 根拠 |
| ---- | ---- | ---- |
| **Buffer 無料 API** | **NG** | Buffer API は read-only ベータ、**TikTok 動画アップロードは API 非対応**、Web アプリの手動投稿のみ ([Buffer Help](https://support.buffer.com/article/595-features-available-on-each-buffer-plan)) |
| **Postiz (OSS)** | **採用** | 公式 REST API (`POST /public/v1/posts`)、TikTok/IG Reels/YT Shorts 30+ 対応、Railway デプロイテンプレあり、**Postiz MCP サーバー**が公開済 ([postiz.com](https://postiz.com/), [Railway template](https://railway.com/deploy/postiz)) |
| **公式 API 直叩き** | 保留 | TikTok Content Posting API は審査 1〜2 週間 + UI 要件 (ユーザー名/アバター/プライバシー選択を投稿前に表示)、未審査は private 制限 ([TikTok docs](https://developers.tiktok.com/doc/content-posting-api-reference-direct-post))。IG Graph API は Business + FB Page 連携必須 |

### Plan A — Postiz セルフホスト (採用)

- **デプロイ先**: Railway ($5 クレジット/月で十分、出先からスマホでも管理画面アクセス可)
- **OAuth 連携**: TikTok / IG (Business) / YouTube を Postiz の管理画面から接続。**Postiz が TikTok の UX 要件を満たした UI を提供しているのが大きい**(自前で TikTok 審査を通す必要がない)
- **自動投稿経路**:
  1. GitHub Actions が `final/9x16/*.mp4` を R2 にアップロード後、その URL を取得
  2. Postiz REST API に `POST /public/v1/posts` (動画 URL + プラットフォーム配列 + scheduled_at)
  3. Postiz が各 SNS の予約キューに投入
- **Bonus: Postiz MCP**: ローカル Claude Code から自然言語で「これ明日 18 時に TikTok に投げて」と指示可能。スマホ運用と相性 ◎

### Plan B — 公式 API 直叩き (Postiz が落ちたら)

- TikTok: 数週間かけて Content Posting API 審査を通す
- IG Reels: Business アカウント化 + FB Page 連携、Graph API v21+ で 3-step publish (POST media → poll status → media_publish)、9:16 / 5-90s / H.264 制約
- YouTube: Data API v3 は比較的素直

### Plan C — 手動フォールバック (常時保険)
- 完成動画 + キャプション + ハッシュタグ JSON を R2 + Notion にアウトプット
- 各アプリの予約機能に手動で流す

## 標準ワークフロー (1ネタが流れる経路)

```
1. content/ideas/20260610-dinner-vpn.md を新規作成 (スマホからでも可)
   ├ Frontmatter: series, hook, length_sec, characters[]
   └ 本文: スクリプト + ショット割り

2. git push → .github/workflows/generate.yml が起動
   ├ orchestrator.py が YAML をパース
   ├ Higgsfield API でショット生成 (画像 → 動画)
   ├ ffmpeg でアセンブル、whisper で字幕タイミング、字幕焼き込み
   ├ virality_predictor でスコアリング
   └ R2 に final/9x16/ アップロード、URL を content/ready/ に commit

3. レビュー (Slack 通知 or GitHub PR コメント)
   ├ 人が確認 → ready/ に PR マージで承認
   └ NG なら ideas/ に差し戻し

4. publish.yml が 1日1回 cron で起動
   ├ ready/ の未投稿を読み、配信スケジュールを決定 (TikTok 即時 / IG +1d / YT +2d)
   ├ Buffer API (or Postiz) に予約投入
   └ archive/ に移動、投稿時刻と URL を記録
```

## シークレット管理

GitHub Repo Secrets:
- `HIGGSFIELD_API_KEY`
- `POSTIZ_BASE_URL` / `POSTIZ_API_KEY` (Plan A)
- TikTok / IG / YT 公式 API トークン (Plan B、必要時のみ)
- `R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY` / `R2_BUCKET`
- `OPENAI_API_KEY` (whisper / 補助)
- `SLACK_WEBHOOK_URL` (任意、通知用)

ローカル開発は `.env.local` (gitignore)。

## コスト想定 (月額)

| 項目 | 想定 |
| ---- | ---- |
| GitHub Actions | $0 (無料枠 2000分) |
| Higgsfield | 既存契約に依存 (本リポ外) |
| R2 ストレージ | $0〜$1 (10GB 以下) |
| Postiz セルフホスト (Railway) | $0〜$5 |
| OpenAI (whisper, 字幕タイミング) | $1〜$3 |
| **合計** | **$5 前後/月** (Higgsfield 別) |

## セキュリティ・安全策

- リポジトリは **private** (公開しない)
- TikTok / IG / YT の API トークンはローテーション可能な状態で保管
- `publish.yml` は **dry-run モード** を最初に通す (実投稿前にログだけ吐く)
- 投稿先・本数のレートリミット (`config/channels.yaml` で 1日上限)
- 全投稿はアーカイブし、`content/archive/` に投稿ログを残す (監査可能性)

## マイルストーン

### Phase 7-α (検証 / 完了分・残り)

**完了**:
- ✅ Buffer 無料 API → NG (read-only、TikTok 動画非対応) と判明、Postiz に切替決定
- ✅ Higgsfield アカウント: Plus プラン、**残 791.8 credits**
- ✅ 推奨モデル選定:
  - **Seedance 2.0** (Bytedance): 参照画像でキャラ一貫性、9:16、4-15s、resolution 480/720/1080p、`genre: comedy` パラメータあり — **メインキャラショット用**
  - **Wan 2.7**: 音声同期 + キャラ一貫、2-15s — **トーキング/口パクショット用**
  - **Higgsfield Preset**: バイラルテンプレ即時適用 — **トランジション/効果カット用**
- ✅ **試作 1 ショット実測完了** (2026-06-06):

  | 項目 | 実測値 |
  | ---- | ------ |
  | soul_2 画像 (2K, 9:16) | **0.12 credits** / 体感 ~30s |
  | Seedance 2.0 動画 (5s, 720p, std, audio on) | **22.5 credits** / 体感 ~5min |
  | 30s ネタ (5s × 6 ショット) 概算 | **~135 credits / 約 30-40 分** |
  | 残 791 credits で作れる本数 | **約 5-6 本** |

  生成物:
  - キャラ参照画像 (job `c5fcfc04…`): https://d8j0ntlcm91z4.cloudfront.net/user_3DHZDwYAr0mvwHad9r4Zby8yRNL/hf_20260606_092013_c5fcfc04-bd00-4093-840b-cb44270069d7.png
  - スタンダップ動画 5s (job `188efc27…`): https://d8j0ntlcm91z4.cloudfront.net/user_3DHZDwYAr0mvwHad9r4Zby8yRNL/hf_20260606_092128_188efc27-a8c1-47ce-a6cd-dec6d9cdef0a.mp4

  プリフライト (`get_cost: true`) が課金実測と完全一致 → CI で予算超過を事前検知可能

- ✅ **ユーザー Higgsfield ワークスペースの既存資産発見** (2026-06-06):

  | 種別 | ID | 説明 |
  | ---- | -- | ---- |
  | Soul Character (trained) | `94133d2e-fcf9-445b-9527-3212f0c9beff` | "Ken Tanaka" — `text2image_soul_v2` 専用 |
  | Reference Element (IP verified) | `ab984578-4915-4cc5-9129-a4781b16d564` | "Ken-Tanaka" — Seedance/Kling/Nano 等で `<<<id>>>` 埋込 |
  | 既存ステージ画像 (soul_v2) | `78a1e5ff-af8f-4271-a311-bf8826445c28` | 青オックス + メガネ + 黒チノのキーフレーム |
  | 既存 Kling 3.0 動画 (15s, 9:16) | `c74806d7-4a93-4eaf-bddd-752ca248e0bb` | プロダクションの先行サンプル |

  → **キャラ "Ken Tanaka" を主役に確定**。シリーズ展開に必要な参照アセット群は既に揃っている

- ⚠️ **環境制約発見**: このサンドボックスから Higgsfield アップロード用 CloudFront ホスト (`d276s3zg8h21b2.cloudfront.net`) への直接 PUT は "Host not in allowlist" でブロック。**GitHub Actions 側でも要確認** (allowlist がなければ問題ないはず、ローカル用クライアントには影響なし)
- ⚠️ Reference Element `<<<id>>>` 埋込は Seedance 2.0 で `Error starting generation` を返す挙動を確認。**現状は start_image 経由が確実**。Element は Nano Banana / Cinema Studio 系で使う方針に切替

**残り**:
1. **Postiz 検証**: Railway に Postiz をデプロイ → TikTok/IG/YT OAuth 接続 → 試験投稿 1 本通すまで
2. **Higgsfield 試作**: Seedance 2.0 で 8 秒 × 3 ショット試作 → 消費クレジット計測 → 1 ネタあたりコスト確定
3. **R2 セットアップ**: アカウント作成 → bucket + IAM
4. **スケルトン**: `scripts/cli.py` でローカル 1 ネタ生成完走

### Phase 7-β (CI 化 / 1 週間)
1. `generate.yml` を GitHub Actions で動かす
2. R2 アップロードと PR 自動作成までつなぐ

### Phase 7-γ (投稿自動化 / 1 週間)
1. Buffer or Postiz の OAuth とトークン管理
2. `publish.yml` を dry-run で通し、その後実投稿
3. 通知 (Slack or GitHub Issue) を追加

### Phase 7-δ (運用最適化 / 継続)
- KPI ダッシュボード (Phase 6 と統合)
- 自動 A/B テスト (同ネタ 2 バリエーション同時投稿)
- ネタ自動提案 (LLM がベンチアカ更新を見て新ネタ案を Issue として起票)

## 検証

- ローカル: `python scripts/cli.py generate content/ideas/sample.md` → `final/9x16/sample.mp4` ができる
- CI: feature ブランチに sample.md を commit → Actions が回って PR がレビュー待ちに立つ
- 投稿: `dry_run=true` で publish.yml を起動 → ログに「投稿予定」が出る → false に切り替えて 1 本だけ実投稿
