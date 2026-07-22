"""GitHub 風の Markdown 表示用スタイル（ライト / ダーク両対応）。"""

# GitHub の配色を再現した CSS。prefers-color-scheme でライト/ダークを自動切替。
GITHUB_CSS = r"""
:root {
  --base-size-16: 16px;
}

/* ===== ライトテーマ ===== */
@media (prefers-color-scheme: light) {
  :root {
    --color-canvas-default: #ffffff;
    --color-canvas-subtle: #f6f8fa;
    --color-border-default: #d1d9e0;
    --color-border-muted: #d1d9e0b3;
    --color-fg-default: #1f2328;
    --color-fg-muted: #59636e;
    --color-accent-fg: #0969da;
    --color-danger-fg: #d1242f;
    --color-neutral-muted: #818b9826;
    --color-code-bg: #f6f8fa;
    --color-blockquote-border: #d1d9e0;
    --color-table-border: #d1d9e0;
    --color-table-alt: #f6f8fa;
    --color-note: #0969da;
    --color-tip: #1a7f37;
    --color-warning: #9a6700;
    --color-important: #8250df;
    --color-caution: #cf222e;
  }
}

/* ===== ダークテーマ ===== */
@media (prefers-color-scheme: dark) {
  :root {
    --color-canvas-default: #0d1117;
    --color-canvas-subtle: #161b22;
    --color-border-default: #3d444d;
    --color-border-muted: #3d444db3;
    --color-fg-default: #e6edf3;
    --color-fg-muted: #9198a1;
    --color-accent-fg: #4493f8;
    --color-danger-fg: #f85149;
    --color-neutral-muted: #656c7633;
    --color-code-bg: #151b23;
    --color-blockquote-border: #3d444d;
    --color-table-border: #3d444d;
    --color-table-alt: #161b22;
    --color-note: #4493f8;
    --color-tip: #3fb950;
    --color-warning: #d29922;
    --color-important: #ab7df8;
    --color-caution: #f85149;
  }
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background-color: var(--color-canvas-default);
  color: var(--color-fg-default);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans",
    Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
  font-size: var(--base-size-16);
  line-height: 1.5;
  word-wrap: break-word;
}

.markdown-body {
  max-width: 1012px;
  margin: 0 auto;
  padding: 32px 48px 128px;
}

/* 見出し */
.markdown-body h1, .markdown-body h2, .markdown-body h3,
.markdown-body h4, .markdown-body h5, .markdown-body h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}
.markdown-body h1 { font-size: 2em; padding-bottom: .3em; border-bottom: 1px solid var(--color-border-muted); }
.markdown-body h2 { font-size: 1.5em; padding-bottom: .3em; border-bottom: 1px solid var(--color-border-muted); }
.markdown-body h3 { font-size: 1.25em; }
.markdown-body h4 { font-size: 1em; }
.markdown-body h5 { font-size: .875em; }
.markdown-body h6 { font-size: .85em; color: var(--color-fg-muted); }

.markdown-body p { margin-top: 0; margin-bottom: 16px; }

.markdown-body a { color: var(--color-accent-fg); text-decoration: none; }
.markdown-body a:hover { text-decoration: underline; }

.markdown-body strong { font-weight: 600; }

/* リスト */
.markdown-body ul, .markdown-body ol { margin-top: 0; margin-bottom: 16px; padding-left: 2em; }
.markdown-body li { margin-top: .25em; }
.markdown-body li > p { margin-top: 16px; }
.markdown-body ul.contains-task-list { list-style: none; padding-left: 0; }
.markdown-body .task-list-item { list-style: none; }
.markdown-body .task-list-item input { margin: 0 .4em .25em -1.4em; vertical-align: middle; }
.markdown-body ul.contains-task-list .task-list-item { padding-left: 1.6em; }

/* コード */
.markdown-body code, .markdown-body tt {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
    "Liberation Mono", monospace;
  font-size: 85%;
  padding: .2em .4em;
  margin: 0;
  background-color: var(--color-neutral-muted);
  border-radius: 6px;
  white-space: break-spaces;
}
.markdown-body pre {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: var(--color-code-bg);
  border-radius: 6px;
  margin-bottom: 16px;
}
.markdown-body pre code {
  padding: 0;
  margin: 0;
  background: transparent;
  border: 0;
  font-size: 100%;
  white-space: pre;
  word-break: normal;
}

/* 引用 */
.markdown-body blockquote {
  margin: 0 0 16px 0;
  padding: 0 1em;
  color: var(--color-fg-muted);
  border-left: .25em solid var(--color-blockquote-border);
}
.markdown-body blockquote > :first-child { margin-top: 0; }
.markdown-body blockquote > :last-child { margin-bottom: 0; }

/* テーブル */
.markdown-body table {
  display: block;
  width: max-content;
  max-width: 100%;
  overflow: auto;
  border-spacing: 0;
  border-collapse: collapse;
  margin-bottom: 16px;
}
.markdown-body table th, .markdown-body table td {
  padding: 6px 13px;
  border: 1px solid var(--color-table-border);
}
.markdown-body table th { font-weight: 600; }
.markdown-body table tr { background-color: var(--color-canvas-default); border-top: 1px solid var(--color-border-muted); }
.markdown-body table tr:nth-child(2n) { background-color: var(--color-table-alt); }

/* 水平線 */
.markdown-body hr {
  height: .25em;
  padding: 0;
  margin: 24px 0;
  background-color: var(--color-border-default);
  border: 0;
}

/* 画像 */
.markdown-body img { max-width: 100%; box-sizing: content-box; }

/* GitHub アラート (> [!NOTE] 等) */
.markdown-body .markdown-alert {
  padding: 8px 16px;
  margin-bottom: 16px;
  border-left: .25em solid var(--color-border-default);
}
.markdown-body .markdown-alert > :first-child { margin-top: 0; }
.markdown-body .markdown-alert > :last-child { margin-bottom: 0; }
.markdown-body .markdown-alert-title {
  display: flex; align-items: center;
  font-weight: 500; line-height: 1;
}
.markdown-body .markdown-alert-note { border-left-color: var(--color-note); }
.markdown-body .markdown-alert-note .markdown-alert-title { color: var(--color-note); }
.markdown-body .markdown-alert-tip { border-left-color: var(--color-tip); }
.markdown-body .markdown-alert-tip .markdown-alert-title { color: var(--color-tip); }
.markdown-body .markdown-alert-warning { border-left-color: var(--color-warning); }
.markdown-body .markdown-alert-warning .markdown-alert-title { color: var(--color-warning); }
.markdown-body .markdown-alert-important { border-left-color: var(--color-important); }
.markdown-body .markdown-alert-important .markdown-alert-title { color: var(--color-important); }
.markdown-body .markdown-alert-caution { border-left-color: var(--color-caution); }
.markdown-body .markdown-alert-caution .markdown-alert-title { color: var(--color-caution); }

/* ===== Pygments シンタックスハイライト ===== */
@media (prefers-color-scheme: light) {
  .markdown-body .highlight .hll { background-color: #ffffcc }
  .markdown-body .highlight .c, .markdown-body .highlight .ch, .markdown-body .highlight .cm,
  .markdown-body .highlight .cp, .markdown-body .highlight .c1, .markdown-body .highlight .cs { color: #6a737d }
  .markdown-body .highlight .k, .markdown-body .highlight .kc, .markdown-body .highlight .kd,
  .markdown-body .highlight .kn, .markdown-body .highlight .kp, .markdown-body .highlight .kr { color: #d73a49 }
  .markdown-body .highlight .kt { color: #d73a49 }
  .markdown-body .highlight .s, .markdown-body .highlight .sa, .markdown-body .highlight .sb,
  .markdown-body .highlight .sc, .markdown-body .highlight .sd, .markdown-body .highlight .s2,
  .markdown-body .highlight .se, .markdown-body .highlight .sh, .markdown-body .highlight .si,
  .markdown-body .highlight .sx, .markdown-body .highlight .sr, .markdown-body .highlight .s1,
  .markdown-body .highlight .ss { color: #032f62 }
  .markdown-body .highlight .m, .markdown-body .highlight .mb, .markdown-body .highlight .mf,
  .markdown-body .highlight .mh, .markdown-body .highlight .mi, .markdown-body .highlight .mo,
  .markdown-body .highlight .il { color: #005cc5 }
  .markdown-body .highlight .n, .markdown-body .highlight .nb { color: #24292e }
  .markdown-body .highlight .nf, .markdown-body .highlight .nx { color: #6f42c1 }
  .markdown-body .highlight .nc, .markdown-body .highlight .nn { color: #6f42c1 }
  .markdown-body .highlight .nt { color: #22863a }
  .markdown-body .highlight .na { color: #6f42c1 }
  .markdown-body .highlight .nv, .markdown-body .highlight .vc, .markdown-body .highlight .vg,
  .markdown-body .highlight .vi { color: #e36209 }
  .markdown-body .highlight .o, .markdown-body .highlight .ow { color: #d73a49 }
  .markdown-body .highlight .gd { color: #b31d28; background-color: #ffeef0 }
  .markdown-body .highlight .gi { color: #22863a; background-color: #f0fff4 }
  .markdown-body .highlight .gh { color: #005cc5; font-weight: bold }
  .markdown-body .highlight .err { color: #b31d28; background-color: #ffeef0 }
}
@media (prefers-color-scheme: dark) {
  .markdown-body .highlight .hll { background-color: #6e7681 }
  .markdown-body .highlight .c, .markdown-body .highlight .ch, .markdown-body .highlight .cm,
  .markdown-body .highlight .cp, .markdown-body .highlight .c1, .markdown-body .highlight .cs { color: #8b949e }
  .markdown-body .highlight .k, .markdown-body .highlight .kc, .markdown-body .highlight .kd,
  .markdown-body .highlight .kn, .markdown-body .highlight .kp, .markdown-body .highlight .kr { color: #ff7b72 }
  .markdown-body .highlight .kt { color: #ff7b72 }
  .markdown-body .highlight .s, .markdown-body .highlight .sa, .markdown-body .highlight .sb,
  .markdown-body .highlight .sc, .markdown-body .highlight .sd, .markdown-body .highlight .s2,
  .markdown-body .highlight .se, .markdown-body .highlight .sh, .markdown-body .highlight .si,
  .markdown-body .highlight .sx, .markdown-body .highlight .sr, .markdown-body .highlight .s1,
  .markdown-body .highlight .ss { color: #a5d6ff }
  .markdown-body .highlight .m, .markdown-body .highlight .mb, .markdown-body .highlight .mf,
  .markdown-body .highlight .mh, .markdown-body .highlight .mi, .markdown-body .highlight .mo,
  .markdown-body .highlight .il { color: #79c0ff }
  .markdown-body .highlight .n { color: #e6edf3 }
  .markdown-body .highlight .nb { color: #79c0ff }
  .markdown-body .highlight .nf, .markdown-body .highlight .nx { color: #d2a8ff }
  .markdown-body .highlight .nc, .markdown-body .highlight .nn { color: #f0883e; font-weight: bold }
  .markdown-body .highlight .nt { color: #7ee787 }
  .markdown-body .highlight .na { color: #79c0ff }
  .markdown-body .highlight .nv, .markdown-body .highlight .vc, .markdown-body .highlight .vg,
  .markdown-body .highlight .vi { color: #ffa657 }
  .markdown-body .highlight .o, .markdown-body .highlight .ow { color: #ff7b72 }
  .markdown-body .highlight .gd { color: #ffdcd7; background-color: #67060c }
  .markdown-body .highlight .gi { color: #aff5b4; background-color: #033a16 }
  .markdown-body .highlight .gh { color: #79c0ff; font-weight: bold }
  .markdown-body .highlight .err { color: #f85149 }
}

/* 空状態（ファイル未選択）の案内 */
.empty-state {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  height: 100vh; color: var(--color-fg-muted);
  text-align: center; padding: 24px;
}
.empty-state h1 { font-size: 1.5em; border: 0; margin-bottom: 8px; color: var(--color-fg-default); }
.empty-state button {
  margin-top: 20px; padding: 8px 20px; font-size: 1em;
  color: #ffffff; background-color: #1f883d;
  border: 1px solid rgba(31,35,40,.15); border-radius: 6px; cursor: pointer;
}
.empty-state button:hover { background-color: #1a7f37; }
.empty-state .hint { margin-top: 16px; font-size: .875em; }
.empty-state kbd {
  padding: 2px 6px; font-size: .85em;
  background-color: var(--color-canvas-subtle);
  border: 1px solid var(--color-border-default);
  border-bottom-width: 2px; border-radius: 6px;
}
"""
