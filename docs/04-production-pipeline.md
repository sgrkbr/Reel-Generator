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

### 3. キャラ/背景/小道具の固定ビジュアル
- **2D カートゥーンスタイル**で生成 (humor_animations 風: フラットカラー、軽い影、太め輪郭、誇張ややあり)
- 主役ペア **Mei & Sam** を Soul Cinematic で学習 (5-20 枚) → soul_id を取得
- `generate_image` で各キャラの正面/横/感情バリエーションを 2D 調プロンプトで生成
- `show_reference_elements` でキャラ単体 + ペアショットを Element 化 (Seedance/Kling 系で `<<<id>>>` 埋込候補だが、現状 Seedance では `start_image` 経由が確実)
- 共通背景 (リビング / 寝室 / キッチン / 玄関 / オフィス) を Nano Banana Pro で 3-5 パターン作成、Reference Element 登録
- Ken Tanaka は補助キャラとして 2D ステ化版を別途生成
- **小道具の一貫性**: ネタに登場する **キーアイテム (チップス袋・マグカップ・スマホ・植物 etc.)** は専用カノニカル画像を作り、シーン生成時に `medias[role:image]` で **キャラ参照と並列で必ず注入**する。text-only では同じ袋デザインが再現できない

### 4. ショット生成
- 各ショットを `generate_video` で 9:16 出力
- 必要に応じ `reframe` で 1:1 / 16:9 派生も作成
- 画質不足は `upscale_video`

### 5. 編集 (CapCut / Premiere)
- カット繋ぎ、SE、BGM
- 英語ワードバイワード字幕 (デカ字、画面下1/3)
- ループ用に最後を冒頭につなげる小ネタ

#### 5a. タイトルカード (新規ネタ全てで標準)
- **0-3s** の冒頭セグメントにタイトル文字を表示
- 配置: **9:16 動画 (1080×1920) の上 1/3、ただし上から 180px の safe zone は避ける**
  - TikTok UI: 上 ~150px と下 ~250px がユーザー名・キャプション・アイコンで隠れる
- スタイル: 太字サンセリフ、白文字 + 黒ストローク 8-12px、シリーズロゴを左肩に小さく
- 例 ("The Loud Snack"): 1 行目 `THE LOUD SNACK` 2 行目 `1:47 AM` (Shot 1 の caption と一体化)

#### 5b. 吹き出し / 心の声テロップ (TTS なし運用)
- **TTS ボイスは現状不要** — 吹き出しテキストで心の声/セリフを表現
- 種類:
  - **Speech bubble (実発話)**: 角丸長方形 + 尻尾、白背景 + 黒ストローク、キャラ口元から
  - **Thought bubble (心の声)**: 雲型 + 小円 3 つの尻尾、キャラ頭上から
  - **On-screen caption (ナレーション/状況説明)**: 画面下 1/3、ワードバイワード karaoke スタイル
- 実装: 編集アプリで PNG/SVG テンプレを各キャラの口元/頭上にフレーム単位で追従配置
- A/B テスト時はテキストだけ差し替え可、再生成不要

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
