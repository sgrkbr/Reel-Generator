# 04. 制作パイプライン (Higgsfield)

Higgsfield MCP を中心とした半自動制作フロー。1本あたり想定リードタイム: 2〜4時間。

## ステップ

### 1. スクリプト
- ネタを 60〜90秒の長尺で書く → ショート用に 25〜45秒へ圧縮
- 最初の3秒に必ずフックを置く (画 / 音 / テキスト のどれか)

### 2. 絵コンテ (Markdown で)
```
[Shot 1] 0-3s  クローズアップ・キャラA驚き顔 — テロップ "My mom said..."
[Shot 2] 3-8s  ワイド・ダイニング — ママのセリフ
...
```

### 3. キャラ/背景の固定ビジュアル
- `generate_image` でキャラ正面/横/感情バリエーションを生成
- `show_characters` / `show_reference_elements` で一貫性アセットとして登録
- 背景は3〜5パターン作って使い回す

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
