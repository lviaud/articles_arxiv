"""Build a small static article collection with Python's standard library."""
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
STYLE = '''
:root { color-scheme: light dark; font-family: system-ui, sans-serif;
  color: #26343d; background: #f7f6f2; }
* { box-sizing: border-box; }
body { margin: 0; }
main { max-width: 78ch; margin: 0 auto; padding: 3.5rem 1.4rem 5rem; }
h1 { font-family: Georgia, serif; font-size: clamp(1.7rem, 4vw, 2.5rem);
  line-height: 1.25; font-weight: 500; margin: 0 0 2.5rem;
  padding-top: 1.4rem; border-top: 3px solid #426b67; text-wrap: balance; }
p { font-size: 1.05rem; line-height: 1.8; margin: 0 0 1.3rem; }
a { color: #245e59; text-underline-offset: .2em; }
ul { padding-left: 1.2rem; line-height: 1.7; }
li { margin: 1rem 0; }
@media (prefers-color-scheme: dark) {
  :root { color: #e4e8e6; background: #182022; }
  a { color: #a2c9c0; }
}
@media print {
  :root { color: #111; background: white; }
  main { max-width: none; padding: 0; }
  h1 { font-size: 22pt; margin-bottom: 1.3rem; }
  p { font-size: 11pt; line-height: 1.5; orphans: 3; widows: 3; }
}
'''

def page(title, content):
    return f'''<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>{STYLE}</style>
</head>
<body><main>{content}</main></body>
</html>
'''

def main():
    OUT.mkdir(exist_ok=True)
    articles = []
    for path in sorted((ROOT / 'articles').glob('*.md')):
        text = path.read_text(encoding='utf-8').strip()
        title_line, body = text.split('\n', 1)
        if not title_line.startswith('# '):
            raise ValueError(f'Missing article title: {path}')
        title = title_line[2:].strip()
        slug = path.stem
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            raise ValueError(f'Invalid article slug: {slug}')
        paragraphs = [' '.join(block.splitlines()) for block in re.split(r'\n\s*\n', body.strip())]
        article = {'title': title, 'slug': slug, 'url': f'{slug}/', 'paragraphs': paragraphs}
        articles.append(article)
        article_dir = OUT / slug
        article_dir.mkdir(exist_ok=True)
        content = '<article><h1>' + escape(title) + '</h1>\n'
        content += '\n'.join('<p>' + escape(p) + '</p>' for p in paragraphs) + '</article>'
        (article_dir / 'index.html').write_text(page(title, content), encoding='utf-8')
    links = '\n'.join(f'<li><a href="{escape(a["url"], quote=True)}">{escape(a["title"])}</a></li>' for a in articles)
    (OUT / 'index.html').write_text(page('Articles', '<h1>Articles</h1><ul>' + links + '</ul>'), encoding='utf-8')
    (OUT / 'articles.json').write_text(json.dumps(articles, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (OUT / '.nojekyll').write_text('', encoding='utf-8')
    print(f'Built {len(articles)} article(s) in {OUT}')

if __name__ == '__main__':
    main()
