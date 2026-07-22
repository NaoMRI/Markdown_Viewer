"""`python md_viewer [ファイル]` のエントリポイント。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__:
    from .app import run
else:
    # `python md_viewer`（ディレクトリ直接実行）ではパッケージ扱いにならないため、
    # 親ディレクトリを import 経路に足して絶対 import に切り替える。
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from md_viewer.app import run


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="md_viewer",
        description="Markdown ファイルを GitHub 風の見た目で閲覧するビューワー。",
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        help="起動時に開く Markdown ファイル（省略時はファイル選択ダイアログを表示）",
    )
    args = parser.parse_args()

    if args.file is not None and not args.file.is_file():
        parser.error(f"ファイルが見つかりません: {args.file}")

    run(args.file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
