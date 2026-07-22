"""Markdown → GitHub 風 HTML の変換。

GitHub 本体と同じ CommonMark + GFM の解釈に揃えるため、markdown-it-py を使う。
"""

from __future__ import annotations

import html
import re
import unicodedata
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from .style import GITHUB_CSS

# GitHub のアラート記法（> [!NOTE] など）で使われる種別と見出し文言
_ALERT_TYPES = {
    "NOTE": "Note",
    "TIP": "Tip",
    "IMPORTANT": "Important",
    "WARNING": "Warning",
    "CAUTION": "Caution",
}

_ALERT_RE = re.compile(r"^\[!(" + "|".join(_ALERT_TYPES) + r")\]\s*$", re.IGNORECASE)

# nowrap=True にして自前で <pre> を組む。markdown-it は "<pre" で始まる結果を
# そのまま採用するため、これで <pre><code> の二重包みを避けられる。
_FORMATTER = HtmlFormatter(nowrap=True)


def _slugify(text: str, _sep: str = "-") -> str:
    """GitHub の見出しアンカーに近い形で slug を作る。"""
    slug = unicodedata.normalize("NFKC", text).strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug, flags=re.UNICODE)
    return re.sub(r"[\s]+", "-", slug)


def _highlight_code(code: str, lang: str, _attrs: str) -> str:
    """コードブロックを Pygments でハイライトする。言語不明ならそのまま出す。"""
    if lang:
        try:
            lexer = get_lexer_by_name(lang, stripall=False)
        except ClassNotFound:
            lexer = None
        if lexer is not None:
            marked = highlight(code, lexer, _FORMATTER)
            return f'<pre class="highlight"><code>{marked}</code></pre>'
    return f'<pre class="highlight"><code>{html.escape(code)}</code></pre>'


def _github_alerts(state) -> None:
    """`> [!NOTE]` 形式の引用を GitHub のアラート表示（div）に変換する。"""
    tokens = state.tokens
    index = 0
    while index < len(tokens) - 2:
        token = tokens[index]
        if token.type != "blockquote_open":
            index += 1
            continue

        paragraph, inline = tokens[index + 1], tokens[index + 2]
        if paragraph.type != "paragraph_open" or inline.type != "inline":
            index += 1
            continue

        children = inline.children or []
        if not children or children[0].type != "text":
            index += 1
            continue

        match = _ALERT_RE.match(children[0].content)
        if match is None:
            index += 1
            continue

        kind = match.group(1).upper()

        # 目印の行と、それに続く改行を本文から取り除く。
        del children[0]
        if children and children[0].type == "softbreak":
            del children[0]
        inline.children = children
        inline.content = inline.content.split("\n", 1)[1] if "\n" in inline.content else ""

        # blockquote を、対応する閉じタグとセットで div に置き換える。
        token.tag = "div"
        token.attrSet("class", f"markdown-alert markdown-alert-{kind.lower()}")
        depth = 0
        for following in tokens[index:]:
            if following.type == "blockquote_open":
                depth += 1
            elif following.type == "blockquote_close":
                depth -= 1
                if depth == 0:
                    following.tag = "div"
                    break

        # 見出し（Note / Warning など）を本文の前に差し込む。
        title_open = tokens[index + 1].copy()
        title_open.attrSet("class", "markdown-alert-title")
        label = Token("text", "", 0)
        label.content = _ALERT_TYPES[kind]
        title_inline = inline.copy()
        title_inline.content = _ALERT_TYPES[kind]
        title_inline.children = [label]
        closer = tokens[index + 3] if index + 3 < len(tokens) else None
        title_close = closer.copy() if closer is not None and closer.type == "paragraph_close" else None

        insert = [title_open, title_inline]
        if title_close is not None:
            insert.append(title_close)
        tokens[index + 1 : index + 1] = insert
        index += 1 + len(insert)

    return None


def _build_parser() -> MarkdownIt:
    """GitHub 相当の機能を有効にした Markdown パーサを組み立てる。"""
    md = (
        MarkdownIt("gfm-like", {"html": True, "linkify": True, "highlight": _highlight_code})
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .use(tasklists_plugin, enabled=False)
        .use(anchors_plugin, max_level=6, slug_func=_slugify)
        .enable("table")
    )
    md.core.ruler.push("github_alerts", _github_alerts)
    return md


_PARSER = _build_parser()


def render_markdown(text: str) -> str:
    """Markdown 文字列を HTML 断片に変換する。"""
    return _PARSER.render(text)


_SHARED_SCRIPT = """
// ⌘O / ⌘R などのショートカット。WebKit 側にメニューが無いため JS で受ける。
document.addEventListener('keydown', function (event) {
  if (!(event.metaKey || event.ctrlKey) || !window.pywebview) return;
  var key = event.key.toLowerCase();
  if (key === 'o') { event.preventDefault(); window.pywebview.api.open_dialog(); }
  else if (key === 'r') { event.preventDefault(); window.pywebview.api.reload(); }
});

// 外部リンクは既定のブラウザで開く（ビューワー内での画面遷移を防ぐ）。
document.addEventListener('click', function (event) {
  var anchor = event.target.closest('a');
  if (!anchor) return;
  var href = anchor.getAttribute('href') || '';
  if (!href || href.startsWith('#')) return;   // ページ内リンクはそのまま
  event.preventDefault();
  if (window.pywebview) { window.pywebview.api.open_link(href); }
});
"""

# 自動リロード時に読書位置を保つため、スクロール量を復元する。
_SCROLL_SCRIPT = """
window.addEventListener('load', function () {
  var saved = %s;
  if (saved > 0) window.scrollTo(0, saved);
});
document.addEventListener('scroll', function () {
  if (window.pywebview) window.pywebview.api.remember_scroll(window.scrollY);
}, { passive: true });
"""


def build_page(body_html: str, title: str, scroll: float = 0) -> str:
    """HTML 断片を、スタイル込みの完全な HTML ページに包む。"""
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>{GITHUB_CSS}</style>
</head>
<body>
<article class="markdown-body">
{body_html}
</article>
<script>
{_SHARED_SCRIPT}
{_SCROLL_SCRIPT % scroll}
</script>
</body>
</html>"""


def render_file(path: Path, scroll: float = 0) -> str:
    """Markdown ファイルを読み込み、完全な HTML ページとして返す。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    return build_page(render_markdown(text), path.name, scroll)


def build_error_page(path: Path, error: Exception) -> str:
    """読み込み・変換に失敗したときのページ。"""
    body = (
        "<h1>ファイルを表示できませんでした</h1>"
        f"<p><code>{html.escape(str(path))}</code></p>"
        f"<pre><code>{html.escape(f'{type(error).__name__}: {error}')}</code></pre>"
    )
    return build_page(body, path.name)


def build_empty_page() -> str:
    """ファイル未選択時に表示する案内ページ。"""
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>Markdown Viewer</title>
<style>{GITHUB_CSS}</style>
</head>
<body>
<div class="empty-state">
  <h1>Markdown Viewer</h1>
  <p>表示する Markdown ファイルを選択してください。</p>
  <button onclick="window.pywebview.api.open_dialog()">ファイルを開く</button>
  <p class="hint"><kbd>⌘O</kbd> でいつでもファイルを開けます　/　<kbd>⌘R</kbd> で再読み込み</p>
</div>
<script>{_SHARED_SCRIPT}</script>
</body>
</html>"""
