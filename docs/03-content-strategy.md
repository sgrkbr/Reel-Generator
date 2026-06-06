# 03. コンテンツ戦略

## ニッチ定義 (一文)

> _Relatable 2D animated couple-life comedy — everyday partner moments, English captions, optimized for TikTok/Reels/Shorts._

主要ベンチマーク: [**@humor_animations** (TikTok, 4.6M / 81.6M likes)](https://www.tiktok.com/@humor_animations) — 2D アニメによる日常あるある (カップル / 職場 / 友達)。我々はこの色味・頭身比・線処理に寄せつつ、最初の主軸を **カップル/パートナーあるある** に絞る。

## ペルソナ / ボイス&トーン

### 主役ペア: **wife & husband** (固有名詞は持たない)

匿名のあだ名で誰でも自分の関係に投影しやすくする — `wife` と `husband` の汎用呼び。脚本でも `WIFE` / `HUSBAND` だけで進める。

- **wife** — 30 代前半、観察眼が鋭くドライ、口で勝ちがち。ふんわりウェーブ + パステル系オーバーサイズトップス。
- **husband** — 30 代前半、物静かでツッコまれ役、内省的なモノローグが得意。短髪 + シンプルなスウェット/Tシャツ。
- ビジュアル: humor_animations 系の大人プロポーション 2D、フラットカラー、内側に線なし、大きめアーモンド目、髪は単色ブロック。
- 設定: 同棲 or 結婚、都市部のマンション暮らし。子なし/ペットなしから始めて、後でペットなどを後付けで足せる余白を残す。

**Higgsfield 資産 (キーフレーム)** — 採用版は `config/characters.yaml` の `pinned_image_jobs` を真として参照。実体は phase 7 で随時更新。

### 声 & トーン
- 視点: 日常恋愛・同棲のあるある (グローバル普遍テーマ)
- 語り口: Self-deprecating + dry observational humor + 思いやり (毒は薄め)
- 差別化軸:
  - 軸1: husband 側の **内省モノローグ**でオチをつくる (humor_animations にあまり無い間)
  - 軸2: 文化普遍 — 固有名詞や特定文化を避け、英語圏すべてに刺さる everyday situation のみ

## シリーズ枠 (humor_animations 流の "枠"、3〜5本)

| シリーズ名 | 一言コンセプト | 想定尺 | 投稿頻度 |
| ---------- | -------------- | ------ | -------- |
| **Couple Things** (主軸) | カップル生活の小さなあるある | **35-55s** | 週 3 本 |
| Inner Voice | husband のモノローグだけで進む 1 人スキット | 25-40s | 週 1 本 |
| Couple WFH | リモートワーク + 同棲のあるある | 35-55s | 週 1 本 |
| Couple Travels | 旅行・帰省・遠出のあるある | 35-55s | 不定期 |

## 30日分ネタリスト ドラフト (Couple Things)

各行: タイトル / 30 秒以内に成立するフック (Hook → Setup → Punch)

1. **"The Loud Snack"** — wife が深夜にチップス袋を開ける / husband は寝室で全部聞いている / オチ: 翌朝 wife "I was being quiet…"
2. **"Two Mugs, One Coffee"** — husband が淹れたコーヒーをカップ移動で奪い合い / 飲んだ瞬間 "It's decaf" → 二人とも顔
3. **"The Shared Calendar"** — wife が husband の予定を勝手に追加 / husband モノローグ "I have a meeting I didn't agree to"
4. **"He Said 'Fine'"** — wife "Are you okay?" / husband "Fine" / 字幕で fine の本当の意味が並ぶ
5. **"Texting in the Same Room"** — お互いソファで同じ家にいるのにスマホでやり取り
6. **"Whose Turn for Dishes"** — 微妙な押し付け合戦 → AI 占いに聞く
7. **"The Closet Side"** — 服が片方の領域を侵食している件
8. **"What Are You Watching"** — 別々の番組を見つつ、結局同じ Reel を見せ合う
9. **"Mom Calls"** — どちらかの母から FaceTime / 隣のパートナーに容赦ない比較質問が飛ぶ
10. **"The Costco Run"** — 1 つだけ買うつもりが全部のサイズアップ
11. **"Plant Parent Dispute"** — wife が植物を増やす / husband "This is the seventh one"
12. **"Bedtime Negotiations"** — 何時に寝るかで暗黙の駆け引き
13. **"The Grocery Trip"** — お互いカゴに違うものを入れていく / レジ前で交渉
14. **"Streaming Subscription Audit"** — 月初に契約整理する儀式
15. **"Whose Family This Weekend"** — 帰省順番のパワーバランス
16. (以降は週次レビューで補充)

### 注: 31〜90 本までのストックは Phase 8 でネタ自動提案を回す予定 (LLM × ベンチアカ更新監視)。

## 禁止/避けるテーマ

- 特定個人 (実在芸能人・政治家) を攻撃するネタ
- 特定の国 / 民族 / 宗教ステレオタイプ (キャラは固有民族設定を持たない)
- センシティブ政治 (グローバル普遍性を損なう)
- 暴言・下ネタ過度 (humor_animations はファミリーセーフ寄り)
- TikTok コミュニティガイドラインに触れる表現
