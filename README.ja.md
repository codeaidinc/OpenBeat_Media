# OpenBeat Media（OSS・PC版）

[English](README.md) · 日本語

**OpenBeat Media** は無料・オープンソースの PC 向け出版ツールです。ジャーナリストが PC 上で記事を編集し、
**ローカルで静的サイトをビルド**して、出力フォルダを **Cloudflare Pages にアップロード**するだけで、
自分のメディアを無料で持てます（git も GitHub アカウントも不要）。

## できること

- 記事の編集（Studio = ローカルの編集UI、または Markdown ファイル直編集）
- 出典トレーサビリティ（出典 URL 必須）、ビート/タグ、著者署名
- 静的サイトのビルド（一覧・記事ページ・RSS フィード）
- テーマ（ロゴ/ヒーロー画像・アクセント色・フォントを `site.json` で差し込み）
- Cloudflare Pages に手動アップロードで公開（無料・サーバーレス）

> 静的サイトです。全記事は公開（ログイン不要・個人データなし・既定でトラッカーなし）。

## 使う

```bash
pip install -r requirements.txt
python cli.py seed        # デモ記事を投入
python cli.py studio      # http://127.0.0.1:5070 で編集
python cli.py build       # output/ に静的サイトを書き出し
# output/ を Cloudflare Pages にドラッグ&ドロップ（docs/Cloudflare_setup.ja.md）
```

> 公開は**ファイルアップロード**（ドラッグ&ドロップ）が既定です。繰り返し配信を
> コード化したい上級者向けに、Terraform で「プロビジョニング＋配信」を一発で行う
> 任意の構成も同梱しています（`deploy/terraform/`）。

## 多言語エディション

記事に `lang` を付けると、`build` は言語ごとにエディションを書き出します
（例 `output/ja/`・`output/en/`）。言語スイッチャー付きで、ルートは主言語
（`site.json` の `primary_lang`）へ誘導します。言語が1種類ならルート直下に書き出します。

## 構成

```
openbeat_media_core/      コアライブラリ（Apache-2.0）
  content.py   Article モデル＋Markdown front-matter 読み書き
  feed.py      RSS/Atom 生成（決定的）
  render.py    記事 -> 静的HTML（テーマ適用・単一/多言語エディション）
  themes/default/  Jinja テーマ（ロゴ/ヒーロー/アクセント色/フォントの slot 付き）
studio.py                 ローカル編集UI（Flask・PyInstaller で Win/Mac 配布）
cli.py                    new / build / studio / seed
content/                  記事（<slug>.md）
docs/Cloudflare_setup.md  公開手順（アカウント作成→ドラッグ&ドロップ→独自ドメイン）
```

## ドキュメントの言語

ドキュメントは**英語が正**で、日本語版を `*.ja.md` として併置します
（例 [`README.md`](README.md)＝英語、本ファイル＝日本語）。

## ライセンス

Apache-2.0（`LICENSE`）。
