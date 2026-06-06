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

## 投稿経路: Buffer 第一 / Postiz フォールバック

### Buffer 経由 (Plan A)
- ユーザーが Buffer 無料アカウントを保有
- **要検証**: 無料プランで TikTok / IG Reels / YT Shorts の動画スケジュール API が叩けるか。Buffer の旧 Publish API は 2023 年 deprecated、新 API は限定アクセス。**Phase 7-α で実機確認**
- 通れば: TypeScript の Buffer SDK で `POST /1/updates/create` 相当を叩き、`scheduled_at` 指定
- 通らなければ → Plan B へ

### Postiz (OSS) 自前ホスト (Plan B)
- [github.com/gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app) を Fly.io / Railway 無料枠でホスト
- TikTok / IG / YT の OAuth 連携を自前で行い、API キーは Postiz が管理
- 自前 SDK 経由で予約投稿
- コスト: 無料枠内で収まる前提 (Fly.io 無料枠 / Railway $5 クレジット)

### Manual fallback (Plan C — 常に用意)
- 完成動画 + キャプション + ハッシュタグ JSON を Google Drive / Notion に出力
- 手動で各アプリの予約機能に流す
- 自動化が失敗してもコンテンツ生産は止めない

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
- `BUFFER_ACCESS_TOKEN` (Plan A)
- `POSTIZ_BASE_URL` / `POSTIZ_TOKEN` (Plan B)
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
| Buffer 無料 / Postiz セルフホスト | $0〜$5 |
| OpenAI (whisper, 字幕タイミング) | $1〜$3 |
| **合計** | **$5 前後/月** (Higgsfield 別) |

## セキュリティ・安全策

- リポジトリは **private** (公開しない)
- TikTok / IG / YT の API トークンはローテーション可能な状態で保管
- `publish.yml` は **dry-run モード** を最初に通す (実投稿前にログだけ吐く)
- 投稿先・本数のレートリミット (`config/channels.yaml` で 1日上限)
- 全投稿はアーカイブし、`content/archive/` に投稿ログを残す (監査可能性)

## マイルストーン

### Phase 7-α (検証 / 1〜2 週間)
1. Buffer 無料プランの API アクセスを実機確認 → Plan A or B 確定
2. Higgsfield API のレートリミットとコストを 1ネタ試作で測定
3. R2 アカウント作成、bucket 作成、IAM 設定
4. リポジトリのスケルトンと `scripts/cli.py` を作って、**ローカルで 1ネタを生成し、ローカルファイルで完成**まで通す

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
