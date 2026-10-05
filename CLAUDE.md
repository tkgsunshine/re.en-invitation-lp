# Re.en（リエン）招待制LP（re.en-invitation-lp）

このプロジェクトは Antigravity(AG) から Claude Code(CC) へ引き継ぎ済み。今後の開発・運用はCCで行う。

## 必読ルール（AG時代から継続）
@.agents/AGENTS.md
@REGULATIONS.md

## Claude Code での運用
- 作業ブランチで変更し、PRで反映する（mainへ直接pushしない）。
- マーケ業務（コラム補充・週次GSCレビュー・記事リライト）は `@marketing-employee`（`.claude/agents/marketing-employee.md`）。詳細は `docs/AI_EMPLOYEE_SETUP.md`。
- **`.github/workflows/` の公開用workflowは本番の仕組みなので、依頼なく変更しない。**
- 少しでも要件が曖昧なときは、推測で進めず先にユーザーへ確認する（`.cursorrules` より継続）。
- Vercelのデプロイは1日100回制限があるため、変更は1回のcommit/pushにまとめる。
- ヒーロー画像・バッジ幅など、レギュレーション記載のデザイン固定値は勝手に変えない。
- 事実は検証してから報告する。依頼のないファイル削除・無関係な改変をしない。
- `.cursorrules` 内のMac絶対パス（`/Users/user/.gemini/...`）は旧環境のもの。画像は `images/` を参照する。


## 担当の線引き（マーケAI社員 / PJ別の開発・運用セッション）
- **マーケAI社員（`@marketing-employee`）**: コラム、記事キュー、SEO（タイトル・説明文・構造化データ・サイトマップ・Search Console分析）を担当する。
- **PJ別の開発・運用セッション**: 機能、画面、運用を担当する。
- **`.github/workflows/` の公開用workflow**: どちらも、ユーザーの依頼がない限り変更しない。
- どちらも、PRで変更する（mainへ直接pushしない）。
- 開発アイデア: ユーザーが新機能・改善のアイデアを話したら、`.claude/agents/dev-employee.md` の「ホーム」の節に従い、ホームのダッシュボード（https://claude.ai/artifact/9eu8jRktA8nGCC8HKN7L8A）の `ideas` に保存する（実装は依頼があるまでしない）。
