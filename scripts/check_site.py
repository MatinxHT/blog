"""Check every generated local link and resource, plus migrated content counts."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
BASE = 'https://martinphysics.club/'
errors = []
formulas = 0


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.formulas = 0
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if 'math-expression' in attrs.get('class', '').split():
            self.formulas += 1
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])


for page in PUBLIC.rglob('*.html'):
    parsed = Links()
    content = page.read_text(encoding='utf-8')
    parsed.feed(content)
    formulas += parsed.formulas
    relative = page.relative_to(PUBLIC).as_posix()
    for link in parsed.links:
        if link.startswith(('mailto:', 'tel:', 'data:', 'javascript:', '#')):
            continue
        url = urlsplit(urljoin(BASE + relative, link))
        if url.hostname != urlsplit(BASE).hostname:
            continue
        path = unquote(url.path)
        target = PUBLIC / path.removeprefix('/')
        if target.is_dir():
            target /= 'index.html'
        if not target.is_file():
            errors.append(f'{relative}: missing target {link}')
    for leftover in ('latex.codecogs.com', '/wp-content/', 'MIGRATIONTOKEN', '{{<'):
        if leftover in content:
            errors.append(f'{relative}: unconverted content {leftover}')

report = json.loads((ROOT / 'scripts/migration/report.json').read_text(encoding='utf-8'))
comments = json.loads((ROOT / 'data/archived_comments.json').read_text(encoding='utf-8'))
for post in report['posts']:
    if not (PUBLIC / post['path'] / 'index.html').is_file():
        errors.append(f'Missing migrated post {post["id"]}')
for slug, entries in comments.items():
    page = PUBLIC / 'posts' / slug / 'index.html'
    if not page.is_file():
        errors.append(f'Missing post for comments: {slug}')
        continue
    content = page.read_text(encoding='utf-8')
    parsed = Links()
    parsed.feed(content)
    for entry in entries:
        if f'comment-{entry["id"]}' not in parsed.ids:
            errors.append(f'Missing rendered comment {entry["id"]} on {slug}')
assert sum(map(len, comments.values())) == report['comment_count']
assert formulas == report['formula_count'], (formulas, report['formula_count'])
assert len(list((ROOT / 'content/posts').glob('wp-*.md'))) == len(report['posts'])
assert not list(PUBLIC.rglob('*.wxr'))
assert not list(PUBLIC.rglob('*WordPress*.xml'))
css = (PUBLIC / 'vendor/katex/katex.min.css').read_text(encoding='utf-8')
for font in re.findall(r'url\((fonts/[^)]+)\)', css):
    if not (PUBLIC / 'vendor/katex' / font).is_file():
        errors.append(f'Missing KaTeX font {font}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f"PASS: {len(report['posts'])} posts, {report['comment_count']} comments, {formulas} formulas, all generated local links and resources resolve.")
