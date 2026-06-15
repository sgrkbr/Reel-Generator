# 11. TikTok Direct Post (Content Posting API)

Couple Things 専用に作った TikTok 投稿ツールの使い方。Sandbox で疎通確認 → 本番審査 → 自動投稿 の順で進める。

---

## 0. 前提

- `docs/09-account-setup.md` と本ドキュメント (`11`) は別系統。`09` は Postiz 経由、こちらは **TikTok 公式 API を直接叩く** ルート。最終的にどちらを採用するかはまだ決めてない (Postiz は審査不要だが UX 要件の制約あり、こちらは審査必要だが完全自動化が可能)。
- このドキュメントは「自前で TikTok for Developers アプリを作って Direct Post する」ルートの実装。`@couplethings_daily` の単一アカウント運用前提。
- 環境変数は `.env`、values は GitHub Pages の `https://sgrkbr.github.io/CoupleThings/` 配信物に依存。

---

## 1. ファイル構成

```
pipelines/publish/tiktok.py        # API クライアント (refresh / init / upload / status / publish_video_file)
scripts/tiktok_auth.py             # 初回 OAuth 認可 (ブラウザ + callback で code 取得)
scripts/tiktok_refresh.py          # access_token を refresh_token で更新
scripts/tiktok_whoami.py           # access_token 疎通確認 (/v2/user/info/)
scripts/tiktok_publish.py          # 動画を Direct Post で投稿 (CLI: video + title)
scripts/make_test_video.py         # 5 秒の 9:16 テスト動画を生成 (ffmpeg via imageio-ffmpeg)
scripts/check_tiktok_env.py        # .env の中身を伏字で表示 (デバッグ用)
scripts/_env_file.py               # .env を壊さず KEY=VALUE を上書き更新するヘルパ
```

`.env` に最低限必要なキー (詳細は `.env.example`):

```
TIKTOK_CLIENT_KEY=...
TIKTOK_CLIENT_SECRET=...
TIKTOK_REDIRECT_URI=https://sgrkbr.github.io/CoupleThings/callback.html
TIKTOK_SCOPES=user.info.basic,video.publish,video.upload
TIKTOK_ACCESS_TOKEN=...         # auth 実行後に自動で入る
TIKTOK_REFRESH_TOKEN=...        # 同上、60 日有効
TIKTOK_OPEN_ID=...              # 同上、アカウント識別子
```

---

## 2. 初回セットアップ (一度きり)

### 2.1 TikTok for Developers アプリ作成
1. https://developers.tiktok.com/ にログイン (couplethings.contact@gmail.com)
2. **Manage apps** → **Connect an app**
3. Production の App details に LP/Privacy/Terms URL を入力 (`https://sgrkbr.github.io/CoupleThings/...`)
4. URL prefix を verify (signature file は `gh-pages` ブランチに置く)
5. **Sandbox** タブで `couplethings-dev` を作成
6. Products に **Login Kit** と **Content Posting API** を追加
7. Content Posting API の詳細で **Direct Post** トグル ON
8. Scopes に `user.info.basic` / `video.publish` / `video.upload` を追加
9. Login Kit の Redirect URI に `https://sgrkbr.github.io/CoupleThings/callback.html`
10. **Target users** に `couplethings_daily` を追加
11. **Apply changes** で保存
12. App details の **Client key / Client secret** を `.env` に転記

### 2.2 ローカル環境
```bash
git checkout claude/tender-cannon-u4zyT
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env
open -e .env   # CLIENT_KEY / CLIENT_SECRET を貼って保存
python scripts/check_tiktok_env.py   # 値が二重 / 空白 になってないか確認
```

### 2.3 OAuth 認可
```bash
python scripts/tiktok_auth.py
```
- ブラウザで TikTok 認可画面が開く
- `couplethings_daily` でログイン → Authorize
- callback ページに着いたら **code** をコピー → ターミナルに貼る → Enter
- **state** も貼る → Enter
- 成功すると `.env` に `TIKTOK_ACCESS_TOKEN` / `TIKTOK_REFRESH_TOKEN` / `TIKTOK_OPEN_ID` が書き込まれる

### 2.4 疎通確認
```bash
python scripts/tiktok_whoami.py
```
HTTP 200 + `display_name: "Couple Things"` が返れば OK。

---

## 3. 動画投稿テスト (Sandbox)

### 3.1 テスト動画を生成
```bash
python scripts/make_test_video.py
# → assets/test/sandbox.mp4 が生成される (5 秒 / 9:16 / 約 100-300 KB)
```

### 3.2 SELF_ONLY で投稿 (sandbox 推奨)
```bash
python scripts/tiktok_publish.py assets/test/sandbox.mp4 --title "sandbox smoke test"
```
- `--privacy SELF_ONLY` がデフォルト (sandbox では自分にだけ見える状態で安全)
- 進行ログ:
  - `[uploading] publish_id=... size=...`
  - `[polling] publish_id=... status=PROCESSING_UPLOAD ...`
  - `[polling] publish_id=... status=PUBLISH_COMPLETE ...`
- 最後に `Done. Final status:` で全フィールド表示

### 3.3 TikTok アプリで確認
`@couplethings_daily` でログインしたスマホの TikTok アプリ →プロフィール → 自分だけ見える投稿の中に上記動画が出ているはず。

---

## 4. トークン期限が切れたとき

`tiktok_publish.py` が `access_token_expired` で落ちたら:
```bash
python scripts/tiktok_refresh.py
python scripts/tiktok_publish.py ...   # 再実行
```

`refresh_token` は使うたびに rotate するので `.env` は毎回自動で書き換わる。

`refresh_token` 自体の期限 (~60 日) を過ぎたら `tiktok_auth.py` から再認可。

---

## 5. Production 審査への流れ

1. Sandbox で 3.x が完走することを確認
2. 同じ操作を画面録画 (Loom / QuickTime, 1-3 分):
   - スクリプト起動
   - ブラウザ認可画面 → Authorize
   - callback ページ
   - ターミナルで publish 完了
   - TikTok アプリで投稿確認
3. TikTok for Developers ポータルの **Production** タブ → **App review**:
   - **Required information** に説明文 (テンプレ済、`docs/10-api-credentials.md` 末尾参照)
   - **Demo video** に上記録画 (mp4, ≤50MB)
   - **Submit for review**
4. 承認後、Production の Client key / Client secret に差し替え (`.env` を更新) → 同じスクリプトで `--privacy PUBLIC_TO_EVERYONE` 指定して本投稿

---

## 6. トラブルシューティング

| 症状 | 原因 / 対処 |
| ---- | ---------- |
| `client_key` エラー (認可画面で) | `.env` の値が `TIKTOK_CLIENT_KEY=TIKTOK_CLIENT_KEY=...` のように二重になってる。`scripts/check_tiktok_env.py` で `has_eq_inside=YES` なら二重。`sed -i '' 's/^TIKTOK_CLIENT_KEY=TIKTOK_CLIENT_KEY=/TIKTOK_CLIENT_KEY=/' .env` で直す |
| `scope_not_authorized` (whoami) | `user.info.profile` が必要なフィールドを要求している。`scripts/tiktok_whoami.py` の `FIELDS` から `username` を外す (現在は外し済み) |
| 認可画面で「ログインできません」 | Sandbox の **Target users** に対象アカウント (`couplethings_daily`) が未追加。ポータルで追加して **Apply changes** |
| `Authorization code is expired` | `tiktok_auth.py` の `code:` プロンプトに時間がかかりすぎた。再実行 |
| 投稿が PUBLISH_FAILED | `fail_reason` フィールドを確認。動画フォーマット (mp4 / mov)、解像度、長さ (sandbox は SELF_ONLY のみ可) を見直す |

---

## 7. 既知の制約 (Sandbox)

- 投稿は **target user 本人にしか見えない** (SELF_ONLY 相当)
- Production 審査未通過の状態では `PUBLIC_TO_EVERYONE` を指定しても落ちる可能性
- Demo video 録画時は SELF_ONLY で OK (TikTok アプリの「自分のみ」表示で十分審査通る)
