"""Check every generated local link and resource, plus migrated content counts."""
import json
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

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
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

report = json.loads((ROOT / 'data/wordpress.json').read_text(encoding='utf-8'))
for post in report['posts']:
    if not (PUBLIC / post['path'] / 'index.html').is_file():
        errors.append(f'Missing migrated post {post["id"]}')
assert formulas == report['formula_count'], (formulas, report['formula_count'])
assert len(list((ROOT / 'content/posts').glob('wp-*.md'))) == len(report['posts'])
assert not list(PUBLIC.rglob('*.wxr'))
assert not list(PUBLIC.rglob('*WordPress*.xml'))
if errors:
    raise SystemExit('\n'.join(errors))
print(f"PASS: {len(report['posts'])} posts, {formulas} formulas, all generated local links and resources resolve.")
