# Cloudflare Pages 公開手順（git も GitHub も不要）

[English](Cloudflare_setup.md) · 日本語

OpenBeat Media Studio で「サイトをビルド」すると `output/` に静的サイトができます。
このフォルダを Cloudflare Pages に**ドラッグ&ドロップ**するだけで公開できます。

## 必要なもの

- Cloudflare の無料アカウント（GitHub アカウントは不要）
- ビルド済みの `output/` フォルダ

## 手順

1. [dash.cloudflare.com](https://dash.cloudflare.com) にログイン。
2. 左メニュー **「Workers & Pages」** → **「Create application」** → **「Pages」** → **「Upload assets」**（直接アップロード）。
3. プロジェクト名を入力（例 `my-beat`）。公開 URL は `<プロジェクト名>.pages.dev` になります。
4. `output/` の中身をドラッグ&ドロップ → **「Deploy site」**。
5. 数十秒で `https://<プロジェクト名>.pages.dev` に公開されます。

> 制限：1回のドラッグ&ドロップは **1,000 ファイル・1ファイル 25 MiB まで**（記事メディアなら十分）。

## 記事を追加・更新したら

1. Studio で編集 → 「サイトをビルド」。
2. 同じ Pages プロジェクトを開き、**新しいデプロイ**として `output/` を再アップロード。

## 独自ドメインを使う（任意）

- `*.pages.dev` は無料。独自ドメイン（例 `news.example.com`）にする場合は、ドメインを取得し
  Pages の **「Custom domains」** から追加（Cloudflare 上の設定は無料、ドメイン代のみ別途）。

## 注意

- 直接アップロード（Direct Upload）を選ぶと、後から Git 連携に切り替えられません（別プロジェクトを作る必要）。
  本ツールは Git を使わない運用なので問題ありません。
