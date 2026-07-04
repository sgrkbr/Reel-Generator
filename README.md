# Reel-Generator

Higgsfield × TikTok 起点で **2D アニメのカップルあるあるショート** (Wife & Husband / 30-60s / 英語・グローバル) を量産し、Instagram Reels と YouTube Shorts へ横展開するための **戦略ドキュメント + 自動化パイプライン** リポジトリ。

参考: TikTok [`@humor_animations`](https://www.tiktok.com/@humor_animations) (4.6M フォロワー)。

## ドキュメント構成

| ファイル | 内容 |
| --- | --- |
| [`docs/01-benchmark-research.md`](docs/01-benchmark-research.md) | お手本アカウント調査 (5〜10件) |
| [`docs/02-pattern-analysis.md`](docs/02-pattern-analysis.md) | バズパターン抽出 (フック / 尺 / 構成 / 投稿頻度) |
| [`docs/03-content-strategy.md`](docs/03-content-strategy.md) | ニッチ定義、ペルソナ、シリーズ案、ネタリスト |
| [`docs/04-production-pipeline.md`](docs/04-production-pipeline.md) | Higgsfield 制作フロー (絵コンテ→画像→動画→編集→字幕) |
| [`docs/05-publishing-workflow.md`](docs/05-publishing-workflow.md) | 3チャネル投稿運用と予約ツール選定 |
| [`docs/06-kpi-and-iteration.md`](docs/06-kpi-and-iteration.md) | KPI と改善サイクル |
| [`docs/07-automation-architecture.md`](docs/07-automation-architecture.md) | 生成 + 投稿の自動化アーキテクチャ |
| [`docs/08-setup.md`](docs/08-setup.md) | Postiz / Cloudflare R2 / GitHub Secrets セットアップ手順 |
| [`docs/09-account-setup.md`](docs/09-account-setup.md) | TikTok / Instagram / YouTube アカウント鞍替え設定 + 必要画像 |
| [`docs/10-api-credentials.md`](docs/10-api-credentials.md) | TikTok / Meta / Google 公式 API クレデンシャル申請手順 |
| [`docs/11-tiktok-direct-post.md`](docs/11-tiktok-direct-post.md) | TikTok Direct Post 投稿パイプライン |
| [`docs/12-monetization-plan.md`](docs/12-monetization-plan.md) | 収益化計画 (5層スタック / ユニットエコノミクス / 収益ゲート) |
| [`docs/13-youtube-shorts-strategy.md`](docs/13-youtube-shorts-strategy.md) | YouTube Shorts 攻略 (ターゲット層 / アルゴリズム / 長尺展開) |

## コード構成

| パス | 役割 |
| --- | --- |
| `pipelines/generate/` | Python: Higgsfield → ffmpeg → R2 のオーケストレーション |
| `pipelines/publish/` | TypeScript: Postiz API で 3 チャネルに予約投稿 |
| `config/` | キャラ / シリーズ / チャネルの YAML 設定 |
| `content/ideas/` | ネタ Markdown (frontmatter + shots) |
| `content/ready/` | 生成完了の reel メタデータ (Postiz 投入待ち) |
| `content/archive/` | 投稿済み |
| `scripts/cli.py` | ローカル用 CLI (`reel generate <slug>` / `reel preflight <slug>`) |
| `.github/workflows/` | `generate.yml` (push → 生成) / `publish.yml` (cron → 予約) |

## ステータス

- [x] Phase 1-4: 戦略・規約ドキュメント (`docs/01`〜`docs/04`)
- [x] Phase 5: 投稿ワークフロー (`docs/05`)
- [ ] Phase 6: KPI と改善 (`docs/06`)
- [x] Phase 7-α: コスト計測 + Postiz 採用 + パイロット試作 (`docs/07`, `docs/08`)
- [x] Phase 7-β: リポスケルトン (`pipelines/`, `config/`, `.github/workflows/`)
- [ ] Phase 7-γ: シークレット投入 + Postiz/R2 デプロイ → 実 CI 稼働 (`docs/08`)
- [ ] Phase 7-δ: KPI ダッシュボード統合 / ネタ自動提案

## スコープ

- ジャンル: 2D アニメ・カップルあるある (ベンチマーク: @humor_animations)
- 主役: **Wife & Husband** (匿名/汎用) — 固有名詞は使わない、誰でも自分ごと化できるように
- 尺: 30-60s / アスペクト比: 9:16
- 言語/市場: 英語 (グローバル)
- 主戦場: TikTok → IG Reels / YouTube Shorts へ横展開
- 投稿運用: 生成 + 投稿を GitHub Actions + Postiz セルフホスト (Railway) で自動化
- 主言語: Python (コア) + TypeScript (薄いスクリプト)
