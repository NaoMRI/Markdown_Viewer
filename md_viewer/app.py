"""Markdown ビューワーのアプリ本体（ウィンドウと操作の管理）。"""

from __future__ import annotations

import subprocess
import threading
import time
import webbrowser
from pathlib import Path

import webview

from .renderer import (
    build_empty_page,
    build_error_page,
    render_file,
)

MARKDOWN_SUFFIXES = (".md", ".markdown", ".mdown", ".mkd", ".mdx", ".txt")
FILE_TYPES = ("Markdown ファイル (*.md;*.markdown;*.mdown;*.mkd;*.mdx;*.txt)", "すべてのファイル (*.*)")

# pywebview 6 で webview.OPEN_DIALOG が非推奨になったため、新しい定数を優先する。
# 参照するだけで警告が出るので、古い定数は FileDialog が無いときだけ触る。
try:
    OPEN_DIALOG = webview.FileDialog.OPEN
except AttributeError:  # pywebview 5 以前
    OPEN_DIALOG = webview.OPEN_DIALOG

# 開いているファイルの更新を監視する間隔（秒）
WATCH_INTERVAL = 1.0


class ViewerApi:
    """WebView の JavaScript から呼び出される API。"""

    def __init__(self) -> None:
        self.window: webview.Window | None = None
        self.current_path: Path | None = None
        self._mtime: float | None = None
        self._scroll: float = 0.0
        self._lock = threading.Lock()

    # ---- JS から呼ばれるメソッド ----

    def open_dialog(self) -> None:
        """ファイル選択ダイアログを開き、選ばれた Markdown を表示する。"""
        if self.window is None:
            return
        start_dir = str(self.current_path.parent) if self.current_path else str(Path.home())
        result = self.window.create_file_dialog(
            OPEN_DIALOG,
            directory=start_dir,
            allow_multiple=False,
            file_types=FILE_TYPES,
        )
        if result:
            self.load(Path(result[0]))

    def reload(self) -> None:
        """開いているファイルを読み込み直す。"""
        if self.current_path is not None:
            self.load(self.current_path, keep_scroll=True)

    def remember_scroll(self, value: float) -> None:
        """自動リロード後に読書位置を復元するため、スクロール量を控えておく。"""
        self._scroll = value or 0.0

    def open_link(self, href: str) -> None:
        """リンクを開く。相対パスの Markdown はビューワー内で、それ以外は外部で開く。"""
        if href.startswith(("http://", "https://", "mailto:")):
            webbrowser.open(href)
            return
        if self.current_path is None:
            return
        target = (self.current_path.parent / href).resolve()
        if target.is_file() and target.suffix.lower() in MARKDOWN_SUFFIXES:
            self.load(target)
        elif target.exists():
            subprocess.run(["open", str(target)], check=False)

    # ---- 内部処理 ----

    def load(self, path: Path, keep_scroll: bool = False) -> None:
        """指定した Markdown ファイルを描画してウィンドウに表示する。"""
        if self.window is None:
            return
        path = path.expanduser().resolve()
        scroll = self._scroll if keep_scroll else 0.0
        try:
            page = render_file(path, scroll)
            mtime = path.stat().st_mtime
        except Exception as error:  # 読み込み失敗もウィンドウ内で伝える
            self.window.load_html(build_error_page(path, error))
            return

        with self._lock:
            self.current_path = path
            self._mtime = mtime
            if not keep_scroll:
                self._scroll = 0.0
        self.window.load_html(page)
        self.window.set_title(f"{path.name} — Markdown Viewer")

    def watch(self) -> None:
        """開いているファイルが更新されたら自動で再描画する（別スレッドで実行）。"""
        while True:
            time.sleep(WATCH_INTERVAL)
            with self._lock:
                path, known_mtime = self.current_path, self._mtime
            if path is None or known_mtime is None:
                continue
            try:
                current_mtime = path.stat().st_mtime
            except OSError:
                continue
            if current_mtime != known_mtime:
                self.load(path, keep_scroll=True)


def run(initial_file: Path | None = None) -> None:
    """ビューワーを起動する。ファイル指定があればそれを開いた状態で始める。"""
    api = ViewerApi()
    window = webview.create_window(
        "Markdown Viewer",
        html=build_empty_page(),
        js_api=api,
        width=1100,
        height=850,
        min_size=(480, 360),
        text_select=True,
    )
    api.window = window

    def on_start() -> None:
        if initial_file is not None:
            api.load(initial_file)
        else:
            api.open_dialog()
        threading.Thread(target=api.watch, daemon=True).start()

    webview.start(on_start, debug=False)
