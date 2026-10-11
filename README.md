# martinphysics.club

站点：<https://martinphysics.club/> 为Hugo 博客，使用 [PaperMod](https://github.com/adityatelange/hugo-PaperMod) 主题。

## 本地调试主页

在 VS Code 的「运行和调试」中选择「博客主页：本地调试」并按 F5。配置优先使用 `.tools/hugo/0.166.0/hugo`，其次使用 PATH 中的 Hugo 0.166.0；还会初始化 PaperMod 子模块、启动包含草稿的本地预览，并在 Chrome 中打开 `http://127.0.0.1:1313/`。首次初始化子模块需要网络连接。调试结束后，在任务终端按 Ctrl+C 停止 Hugo。


## 仓库结构

- `content/draft/`：手稿，使用自己的语言整理、修改和审核内容；整个目录不参与站点构建。
- `content/posts/`：正式发布的文章；`wp-编号` 仅用于维持已公开的文章网址。
- `data/archived_comments.json`：原站已公开评论。
- `layouts/shortcodes/`：本站使用的图片、公式、视频和历史评论组件；`layouts/` 还包含 PaperMod 的 Hugo 兼容覆盖。
- `static/images/`：头像与文章图片；`static/vendor/katex/`：公式渲染所需的精简资源。
- `scripts/`：本地构建与站点检查；`scripts/migration/`：一次性迁移工具及核对清单。
- `themes/PaperMod/`：固定版本的主题子模块；`public/`、`.tools/` 等本地产物已被 Git 忽略。

## 写作流程

先在 `content/draft/` 中用自己方便审核的语言写手稿，使用普通 Markdown，不需要 Hugo front matter。内容修改、审核完成后，再由 AI 根据手稿整理为 `content/posts/` 中的正式正文，补齐发布信息并按要求直接发布。`content/draft/` 是手稿目录，与 Hugo 的 `draft: true` 草稿标记是两回事；即使本地预览启用 `--buildDrafts`，也不会收录手稿。


## 第三方代码

PaperMod 使用 Git submodule 固定版本，遵循其 MIT 许可。
KaTeX 只保留页面运行所需的压缩脚本、样式和 WOFF2 字体，遵循 MIT 许可，见 `static/vendor/katex/LICENSE`。
