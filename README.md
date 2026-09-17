# martinphysics.club

Hugo 博客，使用 [Gokarna](https://github.com/gokarna-theme/gokarna-hugo) 主题。

测试站点：<https://martinphysics.club/>

## 本地运行

安装 Hugo **0.166.0**，然后执行：

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
文章为 `content/posts/wp-*.md`；保留标题、UTC 原始发表/修改时间、分类与标签。
历史文章沿用 WordPress ID 作为稳定路径。访问本站 `?p=100001` 等旧式查询链接会跳转到对应文章。
这不自动重定向旧域名；需要另行配置域名或旧服务器。

图片位于 `static/images/wordpress/`。缩略图引用已替换为备份中的完整图片。
CodeCogs 公式转换为 TeX，由仓库内的 KaTeX 0.16.22 渲染，不请求外部公式图片服务。
视频保留 YouTube 嵌入，播放仍需访问 YouTube。

《Deploy Moonglade Blog System Manually on Linux Server》的一个截图未包含在备份中，旧站读取返回 403；经确认保留文字占位。
迁移清单位于 `data/wordpress.json`，仅包含公开文章清单及资源核对信息。

XML 原件始终保存在仓库之外。`.gitignore` 与 CI 防止加入 XML/WXR 源文件；Hugo 生成的 RSS/sitemap XML 正常发布。
未导入草稿、回收站文章、密码保护内容、默认示例页、隐私政策草稿、评论及 WordPress 账户/系统元数据。

如需重新导入（会覆盖同 ID 文章，请先保存手工修改）：

```sh
python -m pip install -r scripts/requirements.txt
python scripts/migrate_wordpress.py "外部备份目录"
```

## 第三方代码

Gokarna 使用 Git submodule 固定版本，遵循其 GPL-3.0 许可。
KaTeX 遵循 MIT 许可，见 `static/vendor/katex/LICENSE`。
