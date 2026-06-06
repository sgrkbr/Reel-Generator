# 03. コンテンツ戦略

## ニッチ定義 (一文)

> _Relatable 2D animated couple-life comedy — everyday partner moments, English captions, optimized for TikTok/Reels/Shorts._

主要ベンチマーク: [**@humor_animations** (TikTok, 4.6M / 81.6M likes)](https://www.tiktok.com/@humor_animations) — 2D アニメによる日常あるある (カップル / 職場 / 友達)。我々はこの色に寄せつつ、最初の主軸を **カップル/パートナーあるある** に絞る。

## ペルソナ / ボイス&トーン

### 主役ペア (NEW、Phase 7 設計): **Mei & Sam**
- **Mei** — 多人種ミックス (日系 + 欧州系) の女性、30 代前半、IT/デザイン系勤務、観察眼が鋭くドライ、口で勝ちがち。ふんわりカール + パステルカラーのトップス。
- **Sam** — 日系米国人男性、30 代前半、エンジニア寄り、物静かでツッコまれ役、内省的なモノローグが得意。短髪 + シンプル T シャツやスウェット。
- 2D カートゥーン調 (humor_animations の色味: フラットカラー + 軽い影 + 太めの輪郭)
- カップル設定 (結婚 or 同棲) で、日常の小さな衝突・癖・愛情表現を観察ネタに

### 補助キャラ: **Ken Tanaka** (既存 Higgsfield 資産)
- Mei の同僚 / Sam の友達などゲストポジションで登場
- 必要に応じてフォトリアル → 2D ステ化 (Soul Cinematic で再生成)
- Higgsfield 資産:
  - Soul Character (trained): `94133d2e-fcf9-445b-9527-3212f0c9beff`
  - Reference Element (IP verified): `ab984578-4915-4cc5-9129-a4781b16d564`
  - ステージ参照画像: `78a1e5ff-af8f-4271-a311-bf8826445c28`

### 声 & トーン
- 視点: 日常恋愛・同棲のあるある (グローバル普遍テーマ)
- 語り口: Self-deprecating + dry observational humor + 思いやり (毒は薄め)
- 差別化軸:
  - 軸1: アジア系米国人視点で、文化ミックス (英語 + たまの日本語フレーズ / カルチャー要素) を自然に織り込む
  - 軸2: ツッコミより**「内省モノローグ」**を多用 — Sam の心の声がオチを作る

## シリーズ枠 (humor_animations 流の "枠"、3〜5本)

| シリーズ名 | 一言コンセプト | 想定尺 | 投稿頻度 |
| ---------- | -------------- | ------ | -------- |
| **Mei & Sam: Couple Things** (主軸) | カップル生活の小さなあるある | **35-55s** | 週 3 本 |
| Sam's Inner Voice | Sam のモノローグだけで進む 1 人スキット | 25-40s | 週 1 本 |
| Couple vs. Tech | リモートワーク + 同棲のあるある (Ken 同僚役で登場) | 35-55s | 週 1 本 |
| Couple Travels | 旅行・帰省・遠出のあるある | 35-55s | 不定期 |

## 30日分ネタリスト ドラフト (Mei & Sam: Couple Things)

各行: タイトル / 30 秒以内に成立するフック (Hook → Setup → Punch)

1. **"The Loud Snack"** — Mei が深夜のチップス袋を空ける音 / Sam が寝室から無言で目を覚ます / オチ: 翌朝 Mei "I was being quiet…"
2. **"Two Mugs, One Coffee"** — Sam が淹れたコーヒーをカップ移動で奪い合い / 飲んだ瞬間 "It's decaf" → 二人とも顔
3. **"The Shared Calendar"** — Mei が Sam の予定を勝手に追加 / Sam モノローグ "I have a meeting I didn't agree to"
4. **"He Said 'Fine'"** — Mei "Are you okay?" / Sam "Fine" / 字幕で fine の本当の意味が並ぶ
5. **"Texting in the Same Room"** — お互いソファで同じ家にいるのにスマホでやり取り
6. **"Whose Turn for Dishes"** — 微妙な押し付け合戦 → AI 占いに聞く
7. **"The Closet Side"** — 服が片方の領域を侵食している件
8. **"What Are You Watching"** — 別々の番組を見つつ、結局同じ Reel を見せ合う
9. **"Asian Mom Calls"** — Sam の母から FaceTime / Mei に "ちゃんとご飯食べてる?" の質問が降ってくる
10. **"The Costco Run"** — 1 つだけ買うつもりが全部のサイズアップ
11. **"Plant Parent Dispute"** — Mei が植物を増やす / Sam "This is the seventh one"
12. **"Bedtime Negotiations"** — 何時に寝るかで暗黙の駆け引き
13. **"The Trader Joe's Trip"** — お互いカゴに違うものを入れていく / レジ前で交渉
14. **"Streaming Subscription Audit"** — 月初に契約整理する儀式
15. **"Whose Family This Weekend"** — 帰省順番のパワーバランス
16. (以降は週次レビューで補充)

### 注: 31〜90 本までのストックは Phase 8 でネタ自動提案を回す予定 (LLM × ベンチアカ更新監視)。

## 禁止/避けるテーマ

- 特定個人を攻撃するネタ
- センシティブ政治 (グローバル普遍性を損なう)
- 暴言・下ネタ過度 (humor_animations はファミリーセーフ寄り)
- TikTok コミュニティガイドラインに触れる表現

## 禁止/避けるテーマ

- 特定個人を攻撃するネタ
- センシティブ政治
- TikTok コミュニティガイドラインに触れる表現
