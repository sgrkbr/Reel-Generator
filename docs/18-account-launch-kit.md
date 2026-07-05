# 18. アカウント開設キット — The Ledger

docs/13-17 とパイロット制作(docs 内 `assets/pilot/*`)で確立したブランド("THE LEDGER" — ダークネイビー×アンバー×ティールのモーショングラフィックス、Sterling ボイス、比較サイクル+署名指標)を4プラットフォームのアカウントとして開設するための実務キット。**ここに書かれたテキストはそのままコピペで使える形にしてある。**

---

## 0. ブランド一枚要約

| 項目 | 内容 |
| ---- | ---- |
| ブランド名 | **The Ledger** |
| タグライン | *Your money, decoded — every week.* |
| コアコンセプト | 金融・経済の定点観測 + 独自算出の署名指標(Whiplash Index / Breadth Score / $100K Tracker) |
| トーン | 中立・落ち着き・データ第一。煽らない、ポジショントークしない |
| ビジュアル | ダークネイビー(#0B0F16)背景 + アンバー(#FFB03A)アクセント + ティール(#35D9C8)差し色。Archivo Black の極太タイポ |
| ハンドル(共通) | `@theledger.money` (取得状況はプラットフォームごとに§6参照、代替案あり) |

---

## 1. YouTube

| 項目 | 値 |
| ---- | ---- |
| チャンネル名 | **The Ledger** |
| ハンドル | `@theledger.money` |
| チャンネル概要 (About) | ```Your money, decoded — every week.\n\nThe Ledger turns market data into 90-second briefings: what moved, why it matters, and what it means for your money. No hype, no hot takes, no financial advice — just the numbers, explained calmly.\n\n📅 New briefings: Saturday (Week in Money) · Sunday (The Week Ahead) · Wednesday (Money Explained)\n📊 Every quarter: the Whiplash Index, Breadth Score, and $100K Tracker — signature metrics you won't find anywhere else.\n\nNot financial advice. For information only.``` |
| チャンネルキーワード | finance, stock market, economy, personal finance, investing, S&P 500, market news, money explained |
| 動画タイトル規約 | `<フック> \| <シリーズ名>` 例: `What Q2 Did To Your Money \| The Ledger Metrics` |
| 再生リスト | Week in Money / The Week Ahead / Money Explained / The Ledger Metrics (Quarterly) / Year in Review |
| バナー | 2560×1440px、テキストはセーフゾーン(中央 1546×423)に収める。§4 参照 |
| アイコン | 800×800px、正方形ロゴ。§3 参照 |
| 透かし(Subscribe ボタン) | ロゴのみのシンプル版を別途書き出し(§3 candidate 選定後) |

## 2. TikTok

| 項目 | 値 |
| ---- | ---- |
| ユーザー名 | `@theledger.money` (規約上 `.` 可、不可なら `theledgermoney`) |
| 表示名 | **The Ledger** |
| bio (80字以内) | ```Your money, decoded 📊\nNew briefings Sat·Sun·Wed\nNot financial advice ⬇️ link``` |
| プロフィール画像 | 正方形ロゴ(§3) |
| 動画キャプション規約 | `<フック>. <シリーズ名> #shorts #stockmarket #economy` |
| AIGC ラベル | 全動画に TikTok の「AI生成コンテンツ」ラベルを付与(docs/12 §2.2 準拠) |

## 3. Instagram

| 項目 | 値 |
| ---- | ---- |
| ユーザーネーム | `theledger.money` |
| 名前欄 | The Ledger \| Market Briefings |
| bio (150字以内) | ```📊 Your money, decoded — every week\n🗓️ Sat · Sun · Wed briefings\n📈 Quarterly: Whiplash Index, Breadth Score, $100K Tracker\n⚠️ Not financial advice``` |
| リンク | link-in-bio ツール(docs/12 M2 のアフィリエイト導線と共通化) |
| プロフィール画像 | 正方形ロゴ(§3) |
| ハイライト | "Metrics"(署名指標の説明)/ "Schedule"(投稿曜日)/ "FAQ" |
| Reels キャプション規約 | YouTube と同一タイトル + ハッシュタグ3個まで |

## 4. Threads

| 項目 | 値 |
| ---- | ---- |
| ユーザーネーム | Instagram と連携するため自動的に `theledger.money` |
| bio | ```Markets, decoded. No hype, no advice — just the numbers.``` |
| 投稿スタイル | 動画本体の要点1行 + サムネ抜粋画像(スタットタイル1枚をクロップ)+ YT/TikTok へのリンク |
| 用途 | 動画本体は上げず、**署名指標の速報値だけ先出しして本編動画へ誘導**するティザー枠として運用(例: 「Whiplash Index just hit 19.2 — full breakdown tonight」) |

## 5. 共通運用ルール

- **免責表示**: 全動画・全キャプションに "Not financial advice. For information only." を明記(docs/15 §5 準拠)
- **AIGC 開示**: YouTube = 合成メディア開示フラグ、TikTok = AIGC ラベル、Instagram/Threads = キャプション末尾に "🤖 AI-narrated" を付記
- **投稿スケジュール文言**(bio・バナー共通で使う一文): *"New briefings every Saturday, Sunday, and Wednesday. Quarterly deep-dives with our signature metrics."*
- **禁止語**(docs/16 §4 のアンチペルソナ対策): skyrocket, moon, before it's too late, guaranteed, 🚀 の使用禁止

## 6. ハンドル代替案(取得できない場合)

`@theledger.money` が取れない場合の優先順位:

1. `@ledger.metrics`
2. `@weeklyledger`(パイロット制作時の作業用ハンドル。既知)
3. `@theledgerbrief`
4. `@ledger.weekly`

**実際の取得可否はプラットフォームへの登録時に確認が必要**(このセッションからは各プラットフォームへのサインアップ操作ができないため、ここでは確認不可)。

## 7. 必要な画像アセット一覧

| アセット | サイズ | 用途 | 状態 |
| ---- | ---- | ---- | ---- |
| 正方形ロゴ(候補4種) | 1024×1024 | 全プラットフォームのプロフィール画像・アイコン | ✅ 生成済み → `assets/brand/logo1-4.png` |
| バナー背景(候補2種) | 1376×768(→YTは2560×1440にアップスケール) | YouTube バナー、リンクツリーヘッダー | ✅ 生成済み → `assets/brand/banner1-2.png` |
| YouTube サムネテンプレート | 1280×720 | 各動画のサムネ(スタットタイルを流用) | ⬜ 未着手(§8) |
| ファビコン | 512×512 | link-in-bio・将来のウェブサイト用 | ⬜ ロゴ候補から書き出し予定 |

候補画像は GitHub Actions(`brand-assets.yml`)経由で `assets/brand/` にダウンロード済み(このサンドボックスは Higgsfield CDN への直接アクセスがプロキシでブロックされるため、既存パイロットと同じ CI 経由の回避策を使用)。

## 8. 次のアクション

1. [ ] `assets/brand/logo1-4.png` を確認し、1点を正式ロゴとして選定
2. [ ] 選定ロゴを YouTube アイコン(800×800円形セーフエリア)・TikTok/Instagram(1:1)用に書き出し
3. [ ] バナー候補にタグライン("Your money, decoded — every week.")のテキストを合成し、YouTube バナー(2560×1440)を確定
4. [ ] 4プラットフォームで実際にハンドル取得を試行し、§6 の代替順で確保
5. [ ] link-in-bio ツール(Beacons/Linktree)を設置し、Threads・Instagram の bio リンクに接続
6. [ ] docs/09(アカウントセットアップ)を本キットの内容で更新
