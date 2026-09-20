# martinphysics.club

站点：<https://martinphysics.club/> 为Hugo 博客，使用 [PaperMod](https://github.com/adityatelange/hugo-PaperMod) 主题。


## 仓库结构

- `content/posts/`：文章；`wp-编号` 仅用于维持已公开的文章网址。
- `data/archived_comments.json`：原站已公开评论。
- `layouts/shortcodes/`：本站使用的图片、公式、视频和历史评论组件；`layouts/` 还包含 PaperMod 的 Hugo 兼容覆盖。
- `static/images/`：头像与文章图片；`static/vendor/katex/`：公式渲染所需的精简资源。
- `scripts/`：本地构建与站点检查；`scripts/migration/`：一次性迁移工具及核对清单。
- `themes/PaperMod/`：固定版本的主题子模块；`public/`、`.tools/` 等本地产物已被 Git 忽略。


## 第三方代码

PaperMod 使用 Git submodule 固定版本，遵循其 MIT 许可。
KaTeX 只保留页面运行所需的压缩脚本、样式和 WOFF2 字体，遵循 MIT 许可，见 `static/vendor/katex/LICENSE`。
