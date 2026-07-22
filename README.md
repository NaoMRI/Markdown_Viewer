# Markdown Viewer

Mac のプレビュー.app が PDF しか開けない不便さを埋めるための、Markdown 専用ビューワー。
Terminal から起動すると GUI ウィンドウが開き、選んだ Markdown ファイルを
GitHub とほぼ同じ見た目で読める。

## セットアップ

```bash
pip install -r requirements.txt
```

## 使い方

```bash
cd ~/Downloads/Markdown_Reader
python md_viewer                 # 起動と同時にファイル選択ダイアログが開く
python md_viewer test_data.md    # 最初から特定のファイルを開く
```

### どこからでも起動したい場合

`~/.zshrc` に次の行を足すと、どのディレクトリからでも `mdview` で開ける。

```bash
alias mdview='python ~/Downloads/Markdown_Reader/md_viewer'
```

追記後に `source ~/.zshrc` を実行すれば有効になる。

## ウィンドウ内の操作

| 操作 | 内容 |
|------|------|
| `⌘O` | 別の Markdown ファイルを開く |
| `⌘R` | 開いているファイルを読み込み直す |
| リンククリック | 外部 URL は既定のブラウザ、相対パスの `.md` はビューワー内で開く |

ファイルを外部エディタで保存すると、**約1秒で自動的に再描画される**（スクロール位置は保たれる）。
エディタで書きながら隣のウィンドウで仕上がりを確認する使い方ができる。

## 対応している記法

GitHub と同じ CommonMark + GFM の解釈に揃えるため、パーサに markdown-it-py を使っている。

- 見出し・太字・斜体・取り消し線・インラインコード
- テーブル（列ごとの寄せ指定を含む）
- コードブロック（Pygments による言語別シンタックスハイライト）
- タスクリスト `- [x]` / `- [ ]`
- ネストしたリスト（CommonMark 準拠の3スペースインデントも正しく解釈）
- 引用、脚注、水平線、画像
- GitHub のアラート記法 `> [!NOTE]` `> [!TIP]` `> [!IMPORTANT]` `> [!WARNING]` `> [!CAUTION]`
- 生 URL の自動リンク化、YAML フロントマター

macOS のダークモード設定に追従して配色が切り替わる。

## ファイル構成

```
Markdown_Reader/
├── README.md
├── requirements.txt
├── test_data.md            ← 動作確認用のサンプル
└── md_viewer/
    ├── __init__.py
    ├── __main__.py         ← エントリポイント（引数の解釈）
    ├── app.py              ← ウィンドウ管理・ファイル選択・自動リロード
    ├── renderer.py         ← Markdown → HTML の変換
    └── style.py            ← GitHub 風の CSS
```

## 補足

- GUI には pywebview を使い、macOS では OS 標準の WebKit で描画する。
  Electron のような重いランタイムを持たないので起動が速い。
- ローカルの自分のファイルを読む前提のため、Markdown 中の HTML はそのまま描画する。
