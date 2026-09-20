# martinphysics.club

Hugo 博客，使用 [PaperMod](https://github.com/adityatelange/hugo-PaperMod) 主题。

测试站点：<https://martinphysics.club/>

## 仓库结构

- `content/posts/`：文章；`wp-编号` 仅用于维持已公开的文章网址。
- `data/archived_comments.json`：原站已公开评论。
- `layouts/shortcodes/`：本站使用的图片、公式、视频和历史评论组件；`layouts/` 还包含 PaperMod 的 Hugo 兼容覆盖。
- `static/images/`：头像与文章图片；`static/vendor/katex/`：公式渲染所需的精简资源。
- `scripts/`：本地构建与站点检查；`scripts/migration/`：一次性迁移工具及核对清单。
- `themes/PaperMod/`：固定版本的主题子模块；`public/`、`.tools/` 等本地产物已被 Git 忽略。

## 本地运行

在 Windows 版 VS Code 中打开仓库后，通过 **终端 → 运行任务** 选择 **Hugo: 本地预览**；浏览器访问 <http://localhost:1313/>，在任务终端按 `Ctrl+C` 停止。预览包含草稿，保存文件后会自动刷新。

按 `Ctrl+Shift+B` 运行 **Hugo: 构建并检查**，执行与 CI 相同的严格构建和生成站点检查。检查需要本机安装 Python。首次运行会自动初始化主题，并在未找到匹配版本时将 Hugo **0.166.0** 下载到仓库的 `.tools/` 目录（已忽略）。

也可以在 PowerShell 中直接运行：

```powershell
.\scripts\local.ps1 serve
.\scripts\local.ps1 test
```

手动运行 Hugo 的方式：安装 Hugo **0.166.0**，然后执行：

```sh
git submodule update --init --recursive
hugo server
```

构建与检查：

```sh
hugo --gc --minify --panicOnWarning
python scripts/check_site.py
```

## 发布

推送到 `main` 后，GitHub Actions 自动构建并部署至 GitHub Pages。
PR 只构建和检查，不发布。仓库 Settings → Pages 的 Source 使用 GitHub Actions。
当前使用自定义域名 `martinphysics.club`。

## WordPress 迁移

13 篇公开文章、11 张原始图片及 52 个公式已迁移。
文章位于 `content/posts/`；保留标题和 UTC 原始发表/修改时间。分类与标签根据文章内容重新整理。
历史文章沿用 WordPress ID 作为稳定路径。访问本站 `?p=100001` 等旧式查询链接会跳转到对应文章。
这不自动重定向旧域名；需要另行配置域名或旧服务器。

文章图片位于 `static/images/posts/`，站点头像位于 `static/images/avatar.jpg`。缩略图引用已替换为备份中的完整图片。
CodeCogs 公式转换为 TeX，由仓库内的 KaTeX 0.16.22 渲染，不请求外部公式图片服务。
视频保留 YouTube 嵌入，播放仍需访问 YouTube。

《Deploy Moonglade Blog System Manually on Linux Server》的一个截图未包含在备份中，旧站读取返回 403；经确认保留文字占位。
迁移工具与核对清单集中在 `scripts/migration/`，清单仅包含公开文章及资源核对信息。已批准的 3 条公开评论保存在 `data/archived_comments.json`，会显示在对应文章的「历史评论」区；评论邮箱、IP 等非公开信息未导入。回收站示例文章的默认评论未导入。

XML 原件始终保存在仓库之外。`.gitignore` 与 CI 防止加入 XML/WXR 源文件；Hugo 生成的 RSS/sitemap XML 正常发布。
未导入草稿、回收站文章、密码保护内容、默认示例页、隐私政策草稿及 WordPress 账户/系统元数据。

如需重新导入（会覆盖同 ID 文章，请先保存手工修改）：

```sh
python -m pip install -r scripts/migration/requirements.txt
python scripts/migration/import_wordpress.py "外部备份目录"
```

## 第三方代码

PaperMod 使用 Git submodule 固定版本，遵循其 MIT 许可。
KaTeX 只保留页面运行所需的压缩脚本、样式和 WOFF2 字体，遵循 MIT 许可，见 `static/vendor/katex/LICENSE`。
