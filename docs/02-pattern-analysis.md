# 02. パターン分析

`01-benchmark-research.md` のデータから「勝ち筋テンプレート」を3〜5個抽出する。

## 抽出フレーム

各テンプレートを次の項目で整理する。

- **テンプレ名**:
- **再現する構成 (秒単位)**: 例 `0-3s フック / 3-8s セットアップ / 8-25s 展開 / 25-30s オチ`
- **ビジュアル方式**: 一枚絵ズーム / 2キャラ切り替え / アバター語り 等
- **音声方式**: 本人声 / AI TTS / 既存音源
- **字幕スタイル**:
- **Higgsfield で再現するときの設定**:
  - 使うモデル (`models_explore` で確認)
  - プリセット (`presets_show`)
  - キャラ一貫性 (`show_characters` / `show_reference_elements`)
- **適した尺**:
- **再現難易度 / コスト**:

## プライマリ・ベンチマーク (確定): [@humor_animations](https://www.tiktok.com/@humor_animations)

- 4.6M followers / 81.6M likes
- 2D アニメ・everyday humor (カップル / 職場 / 友達)
- 尺: **30-60s**
- 我々の最初のシリーズはこの色味 & フォーマット感に寄せる

## テンプレート候補

### Template A: Couple Skit (主軸)
- **構成 (40s 例)**: `0-3s フック (片方の異常行動を別キャラ視点で観察)` → `3-15s セットアップ` → `15-30s ヒート/オチへの加速` → `30-40s オチ + ループ用フェード`
- **ビジュアル方式**: 2D カートゥーン、固定の家空間 (リビング/寝室/キッチン) で 2 キャラ会話、たまにモノローグでカットイン
- **音声方式**: 英語 TTS (Cinema Studio Video の音声同期、または whisper SRT で焼き) + 軽い BGM
- **字幕**: ワードバイワード karaoke、白字 + 黒ストローク、画面下 1/3
- **Higgsfield 設定**:
  - キーフレーム生成: `soul_cinematic` / `nano_banana_2` (2D 風の指示)
  - 動画化: `seedance_2_0` を `start_image` 経由 (multi-shot は次フェーズで `kling3_0` も検討)
  - 一貫性: 各キャラを Soul Cinematic で学習、Reference Element でも保持
- **適した尺**: 35-55s
- **再現難易度 / コスト**: 中 (1 ネタ ~150-180 credits)

### Template B: Inner Monologue (Self-deprecating 1 人)
- **構成 (25s)**: `0-2s 表情アップ + テキスト "I should not say this..."` → `2-20s 心の声 + シーンの反復` → `20-25s 言葉に出した瞬間 + 相手の反応`
- 1 キャラのみ生成で済むのでコスト低い (~80 credits)

### Template C: Title-Card Franchise ("If [X] were a couple thing")
- Steven He "If X were Asian" の couple 版
- カード "If THIS were a couple thing — Day 14" → 寸劇 → コミカルなオチ
- 連番タイトル化することで series identity を作る

## 共通バズ要素チェックリスト

- [ ] 3秒以内に強いビジュアル or テキストフック
- [ ] 1動画1テーマ
- [ ] 8〜12秒に1回ボケ/展開
- [ ] オチで黒画面+テロップ or 余韻
- [ ] ワードバイワードの大きな英語字幕
- [ ] ループしやすい構造
