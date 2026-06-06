# 04. 制作パイプライン (Higgsfield)

Higgsfield MCP を中心とした半自動制作フロー。1本あたり想定リードタイム: 2〜4時間。

## ステップ

### 1. スクリプト
- ネタを 60〜90秒の長尺で書く → **30-60s 目安** (humor_animations 系の主流尺) に圧縮
- 最初の3秒に必ずフックを置く (画 / 音 / テキスト のどれか)
- カップルスキットは「片方の異常行動 → 相手のリアクション → モノローグオチ」のテンプレに当てる

### 2. 絵コンテ (Markdown で)
```
[Shot 1] 0-3s  クローズアップ・キャラA驚き顔 — テロップ "My mom said..."
[Shot 2] 3-8s  ワイド・ダイニング — ママのセリフ
...
```

### 3. キャラ/背景の固定ビジュアル
- **2D カートゥーンスタイル**で生成 (humor_animations 風: フラットカラー、軽い影、太め輪郭、誇張ややあり)
- 主役ペア **Mei & Sam** を Soul Cinematic で学習 (5-20 枚) → soul_id を取得
- `generate_image` で各キャラの正面/横/感情バリエーションを 2D 調プロンプトで生成
- `show_reference_elements` でキャラ単体 + ペアショットを Element 化 (Seedance/Kling 系で `<<<id>>>` 埋込候補だが、現状 Seedance では `start_image` 経由が確実)
- 共通背景 (リビング / 寝室 / キッチン / 玄関 / オフィス) を Nano Banana Pro で 3-5 パターン作成、Reference Element 登録
- Ken Tanaka は補助キャラとして 2D ステ化版を別途生成

### 4. ショット生成
- 各ショットを `generate_video` で 9:16 出力
- 必要に応じ `reframe` で 1:1 / 16:9 派生も作成
- 画質不足は `upscale_video`

### 5. 編集 (CapCut / Premiere)
- カット繋ぎ、SE、BGM
- 英語ワードバイワード字幕 (デカ字、画面下1/3)
- ループ用に最後を冒頭につなげる小ネタ

### 6. 公開前チェック
- `virality_predictor` でスコアリング
- フック弱 / 維持率予測低 → Shot1 を作り直し
- 字幕の誤字、音割れ、著作権素材の混入チェック

## ファイル管理ルール

```
assets/
  characters/      # 一貫性アセット (画像)
  backgrounds/
raw/
  YYYYMMDD-slug/   # 1ネタ1フォルダ
    script.md
    storyboard.md
    shots/         # generate_video 出力
final/
  9x16/            # TikTok / Reels / Shorts 縦
  1x1/             # IG フィード補助
thumbs/
```

## 命名規則

`YYYYMMDD-series-slug-vN.mp4` 例: `20260610-dinner-mom-vpn-v2.mp4`
