"""UI strings (English-first, with a Japanese option).

- SITE: chrome of the generated static site (theme). Picked per edition language,
  so /en/ shows English chrome and /ja/ shows Japanese chrome.
- STUDIO: the local Studio editing UI and CLI messages. English by default;
  set the environment variable OPENBEAT_LANG=ja for Japanese.
"""
from __future__ import annotations

import os

SITE = {
    "en": {
        "lang": "en",
        "rss": "RSS feed",
        "site_desc": "A sourced static publication",
        "sponsors": "Sponsors",
        "latest": "Latest",
        "editorial": "Editorial",
        "sources_h": "Sources",
        "related": "Related",
        "other": "Other",
        "no_articles": "No articles yet.",
        "src_pre": "",
        "src_post": " sources",
        "sec_post": " articles",
        "back_pre": "← Back to ",
        "back_post": "",
    },
    "ja": {
        "lang": "ja",
        "rss": "RSS フィード",
        "site_desc": "出典付きの静的メディア",
        "sponsors": "協賛",
        "latest": "最新",
        "editorial": "編集部",
        "sources_h": "出典",
        "related": "関連記事",
        "other": "その他",
        "no_articles": "まだ記事がありません。",
        "src_pre": "出典 ",
        "src_post": " 件",
        "sec_post": " 本",
        "back_pre": "← ",
        "back_post": " トップへ",
    },
}

STUDIO = {
    "en": {
        "studio_title": "OpenBeat Media Studio",
        "new_article": "+ New article",
        "build_site": "Build site",
        "preview": "Preview",
        "edit": "Edit",
        "delete": "Delete",
        "confirm_delete": "Delete this article?",
        "no_articles": "No articles yet. Start with “+ New article”.",
        "hint": "Publish: (1) write articles → (2) Build site → (3) drag & drop the output folder",
        "hint2": "onto Cloudflare Pages (no git, no GitHub). See docs/Cloudflare_setup.md.",
        "sources_unit": "sources",
        "edit_article": "Edit article",
        "f_title": "Title *",
        "f_summary": "Summary (excerpt for the index and feed)",
        "f_beat": "Beat (e.g. science-tech / food-agriculture / climate-energy)",
        "f_tags": "Tags (comma-separated)",
        "f_author": "Author",
        "f_sources": "Source URLs * (comma- or newline-separated, at least one)",
        "f_published": "Published at (empty = now; e.g. 2026-06-14T09:00:00Z)",
        "f_body": "Body (Markdown)",
        "save": "Save",
        "back_to_list": "← Back to list",
        "source_note": "A source is required (OpenBeat source traceability).",
        "msg_title_required": "Title is required",
        "msg_sources_required": "A source is required (source traceability)",
        "msg_saved": "Saved: {slug}",
        "msg_deleted": "Deleted: {slug}",
        "msg_built": "Build complete: {n} article(s){extra} → {dir} (upload this folder to Cloudflare)",
        "msg_build_first": "Build the site first",
        "editions_note": " · {n} editions ({langs})",
    },
    "ja": {
        "studio_title": "OpenBeat Media Studio",
        "new_article": "＋ 新規記事",
        "build_site": "サイトをビルド",
        "preview": "プレビュー",
        "edit": "編集",
        "delete": "削除",
        "confirm_delete": "削除しますか？",
        "no_articles": "記事がありません。「＋ 新規記事」から始めましょう。",
        "hint": "公開手順：① 記事を書く → ②「サイトをビルド」→ ③ 出力フォルダ",
        "hint2": "を Cloudflare Pages にドラッグ＆ドロップ（git も GitHub も不要）。詳細は docs/Cloudflare_setup.md。",
        "sources_unit": "出典",
        "edit_article": "記事を編集",
        "f_title": "タイトル *",
        "f_summary": "要約（一覧・フィードの抜粋）",
        "f_beat": "ビート（例: science-tech / food-agriculture / climate-energy）",
        "f_tags": "タグ（カンマ区切り）",
        "f_author": "著者",
        "f_sources": "出典 URL *（カンマか改行区切り・1つ以上）",
        "f_published": "公開日時（空なら現在時刻・例 2026-06-14T09:00:00Z）",
        "f_body": "本文（Markdown）",
        "save": "保存",
        "back_to_list": "← 一覧へ",
        "source_note": "出典は必須です（OpenBeat の出典トレーサビリティ）。",
        "msg_title_required": "タイトルは必須です",
        "msg_sources_required": "出典は必須です（出典トレーサビリティ）",
        "msg_saved": "保存しました: {slug}",
        "msg_deleted": "削除しました: {slug}",
        "msg_built": "ビルド完了: {n} 本{extra} → {dir}（このフォルダを Cloudflare にアップロード）",
        "msg_build_first": "先に「ビルド」してください",
        "editions_note": "・{n}版（{langs}）",
    },
}


def get_lang() -> str:
    """Studio / CLI language. English by default; OPENBEAT_LANG=ja for Japanese."""
    lang = (os.environ.get("OPENBEAT_LANG") or "en").lower()[:2]
    return lang if lang in STUDIO else "en"


def site_ui(lang) -> dict:
    """Site-chrome strings for the given edition language (falls back to English)."""
    return SITE.get((lang or "en")[:2], SITE["en"])


def studio_ui(lang=None) -> dict:
    """Studio / CLI strings (defaults to get_lang())."""
    lang = lang or get_lang()
    return STUDIO.get((lang or "en")[:2], STUDIO["en"])
