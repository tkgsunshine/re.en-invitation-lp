# マーケAI社員 引き継ぎ・運用ガイド（Re.en）

## 役割分担
| 項目 | 担当 | 仕組み |
|---|---|---|
| コラムの公開 | GitHub Actions | `auto-publish.yml`（10:00 / 18:00 JST）と `daily_column.yml`（8:05 / 17:05 JST ほか）が `run_matching_column_pipeline.py` を実行。4時間の二重投稿ガード付き |
| コラムの補充 | Claude Code（マーケAI社員） | `editorial_calendar_matching.json` に記事を追記（未公開10本を維持） |
| 検索データの分析 | GitHub Actions ＋ Claude Code | 毎週月曜9:07 JSTに `docs/marketing/weekly/` へレポートを出力 → AI社員が改善案を作成 |

AI社員の定義: `.claude/agents/marketing-employee.md`（`@marketing-employee` で呼び出し）

## 手書き記事の保護（重要）
`rewrite_all_columns_rich.py` は、毎回すべての記事本文を、タイトルを差し込んだ定型文に書き換える。手書きの記事を守るため、カレンダーのエントリに `"authored": true` を付ける。公開時に `<!-- authored:cc -->` が本文に入り、定型文の書き換えの対象から外れる。

## 週次GSCレポートの有効化（人間の作業）
1. Search Console API を有効にしたサービスアカウントのJSONキーを用意
2. Search Console の「設定 > ユーザーと権限」で、`re-en.jp` のプロパティにそのサービスアカウントのメールを追加（権限は「制限付き」でよい）
3. GitHub Settings > Secrets に `GSC_CREDENTIALS`（JSON全文）を登録
4. Variables に `GSC_SITE_URL`（例 `sc-domain:re-en.jp`。URLプレフィックスなら `https://re-en.jp/`）
5. Actions タブから "Weekly GSC Report" を手動実行して確認

## AG（Antigravity）側の運用
- AGの自動コラム設定は止める。ただし **`.github/workflows/` の2つのworkflowは公開の本番の仕組みなので変更しない**
- リポジトリへの変更は、直接mainへpushせずPRで行う
