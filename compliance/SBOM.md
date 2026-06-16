> 本書はリーガルチェック前のドラフト（標準構成）です。弁護士確認のうえ確定してください。

# SBOM — OpenBeat Media（無料OSS版） / Software Bill of Materials

製品ライセンス：Apache-2.0（`LICENSE` / `NOTICE` 参照）。
本SBOMは `requirements.txt` および `requirements-dev.txt` に基づきます。

## 直接依存（実行時 / Runtime — `requirements.txt`）

| パッケージ | 宣言バージョン | 用途 | ライセンス |
|---|---|---|---|
| Flask | `>=3.0` | ローカル「Studio」のWebアプリ（記事編集UI、127.0.0.1）。生成サイトには同梱されない | BSD-3-Clause |
| Jinja2 | `>=3.1` | テーマ（`themes/default/*.html`）のHTMLテンプレートエンジン。静的サイト生成に使用 | BSD-3-Clause |
| markdown | `>=3.5`（任意） | 記事本文の Markdown→HTML 変換（高品質）。無い場合は内蔵の最小フォールバック | BSD-3-Clause |

## 推移的依存（主要 / Transitive — 自動導入）

| パッケージ | 由来 | 用途 | ライセンス |
|---|---|---|---|
| Werkzeug | Flask | WSGI ユーティリティ（ローカルサーバ） | BSD-3-Clause |
| Jinja2 | Flask | （上記、Flask も依存） | BSD-3-Clause |
| MarkupSafe | Jinja2 / Flask | HTML エスケープ（XSS対策） | BSD-3-Clause |
| click | Flask | CLI | BSD-3-Clause |
| itsdangerous | Flask | flash メッセージ等の署名（secret_key 利用） | BSD-3-Clause |
| blinker | Flask | シグナル | MIT |

## 開発専用（Dev only — `requirements-dev.txt`、配布物に非同梱）

| パッケージ | 宣言バージョン | 用途 | ライセンス |
|---|---|---|---|
| pytest | `>=8.0` | テスト実行（`tests/`） | MIT |

## メモ
- **生成される公開サイトは静的HTML/CSSのみ**で、上記ランタイム依存（Flask/Jinja2 等）を**含みません**。依存はローカルの編集・ビルド時のみ動作します。
- ネットワーク送信・テレメトリ・AIモデル依存はありません。
- 正確なバージョン固定が必要な場合は、ビルド環境で `pip freeze` を取得し本SBOMに追記してください。

## ギャップ（要記入）
- 【固定バージョン（`pip freeze` 出力）の貼り付け】
- 【markdown を同梱／非同梱どちらで配布するかの確定】
