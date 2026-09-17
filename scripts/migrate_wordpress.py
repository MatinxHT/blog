"""Import only public WordPress posts; keep the WXR source outside this repo."""
import argparse
import html
import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
from markdownify import markdownify

NS = {"wp": "http://wordpress.org/export/1.2/", "content": "http://purl.org/rss/1.0/modules/content/"}
ROOT = Path(__file__).resolve().parents[1]


def migrate(source):
    source = source.resolve()
    if source.is_relative_to(ROOT):
        raise ValueError("Keep the WordPress export outside the public repository")
    exports = list(source.glob("*.xml"))
    if len(exports) != 1:
        raise ValueError("Expected exactly one WordPress XML export")
    channel = ET.parse(exports[0]).find("channel")
    images = ROOT / "static/images/wordpress"
    images.mkdir(parents=True, exist_ok=True)
    files = {p.name: p for p in source.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}}
    for name, path in files.items():
        shutil.copy2(path, images / name)
    report = {"posts": [], "images": sorted(files), "formula_count": 0, "missing_images": [], "excluded": {}}
    posts = [i for i in channel.findall("item") if i.findtext("wp:post_type", namespaces=NS) == "post" and i.findtext("wp:status", namespaces=NS) == "publish" and not i.findtext("wp:post_password", namespaces=NS)]
    ids = {i.findtext("wp:post_id", namespaces=NS) for i in posts}
    for item in channel.findall("item"):
        if item not in posts:
            key = item.findtext("wp:post_type", namespaces=NS) + ":" + item.findtext("wp:status", namespaces=NS)
            report["excluded"][key] = report["excluded"].get(key, 0) + 1
    for item in posts:
        post_id = item.findtext("wp:post_id", namespaces=NS)
        title = item.findtext("title")
        body = item.findtext("content:encoded", default="", namespaces=NS)
        soup = BeautifulSoup(body, "html.parser")
        replacements = {}

        def protect(node, value):
            token = f"MIGRATIONTOKEN{len(replacements)}END"
            replacements[token] = value
            node.replace_with(token)

        for node in list(soup.find_all("img")):
            src = html.unescape(node.get("src", ""))
            if "latex.codecogs.com/" in src:
                tex = html.unescape(unquote(src.split("?", 1)[1])).replace("&space;", " ").replace("&plus;", "+")
                display = "aligncenter" in node.get("class", []) or (node.parent and "text-align: center" in node.parent.get("style", ""))
                protect(node, '{{< math display="' + str(display).lower() + '" >}}' + tex + '{{< /math >}}')
                report["formula_count"] += 1
                continue
            name = unquote(urlsplit(src).path.rsplit("/", 1)[-1])
            if name not in files:
                name = re.sub(r"-\d+x\d+(?=\.[^.]+$)", "", name)
            if name in files:
                alt = node.get("alt") or Path(name).stem
                protect(node, '{{< image src=' + json.dumps("images/wordpress/" + name, ensure_ascii=False) + ' alt=' + json.dumps(alt, ensure_ascii=False) + ' >}}')
            else:
                report["missing_images"].append({"post_id": post_id, "source": src})
                protect(node, '\n\n> **图片待恢复：** 原文此处的截图未包含在 WordPress 备份中。\n\n')
        for node in list(soup.find_all("iframe")):
            src = node.get("src", "")
            if "youtube.com/embed/" not in src:
                raise ValueError(f"Unsupported embed in post {post_id}")
            video = urlsplit(src).path.rsplit("/", 1)[-1]
            start = re.search(r"[?&]t=(\d+)s?", src)
            protect(node, '\n\n{{< video id="' + video + '" start="' + (start[1] if start else "0") + '" >}}\n\n')
        for node in list(soup.find_all("pre")):
            cls = " ".join(node.get("class", []) + (node.code.get("class", []) if node.code else []))
            language = re.search(r"language-([\w+-]+)", cls)
            code = node.get_text()
            fence = "`" * max(3, max((len(m[0]) + 1 for m in re.finditer(r"`+", code)), default=3))
            protect(node, "\n\n" + fence + (language[1] if language else "text") + "\n" + code.strip("\n") + "\n" + fence + "\n\n")
        for node in soup.find_all("a", href=True):
            href = html.unescape(node["href"])
            match = re.search(r"[?&]p=(\d+)", href)
            if match and match[1] in ids and urlsplit(href).hostname == "martinphysics.club":
                node["href"] = '{{< ref "posts/wp-' + match[1] + '.md" >}}'
        markdown = markdownify(str(soup), heading_style="ATX", bullets="-", escape_underscores=False)
        for token, value in replacements.items():
            markdown = markdown.replace(token, value)
        date = item.findtext("wp:post_date_gmt", namespaces=NS)
        if not date or date.startswith("0000"):
            raise ValueError(f"Missing UTC date for {post_id}")
        modified = item.findtext("wp:post_modified_gmt", namespaces=NS)
        front = {"title": title, "date": date.replace(" ", "T") + "Z", "draft": False, "type": "post", "slug": "wp-" + post_id, "wordpress_id": int(post_id), "tags": [c.text for c in item.findall("category") if c.get("domain") == "post_tag"], "categories": [c.text for c in item.findall("category") if c.get("domain") == "category"]}
        if modified and not modified.startswith("0000"):
            front["lastmod"] = modified.replace(" ", "T") + "Z"
        out = ROOT / "content/posts" / ("wp-" + post_id + ".md")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(front, ensure_ascii=False, indent=2) + "\n\n" + markdown.strip() + "\n", encoding="utf-8")
        report["posts"].append({"id": int(post_id), "title": title, "path": "posts/wp-" + post_id + "/"})
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data/wordpress.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(posts)} posts, {len(files)} images, {report['formula_count']} formulas; missing images: {len(report['missing_images'])}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    migrate(parser.parse_args().source)
