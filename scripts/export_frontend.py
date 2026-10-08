"""Export Django pages for the repository's standalone Vite preview."""
import json
import os
import re
import shutil
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mono.settings')
import django
django.setup()
from django.test import Client
client = Client(HTTP_HOST='localhost')
pages = {}
for route in ['/', '/villa/', '/explore-villa/', '/rooms/', '/activities/', '/about/', '/our-story/', '/contact/', '/cookie-policy/', '/privacy-policy/', '/terms-and-conditions/']:
    response = client.get(route)
    assert response.status_code == 200, (route, response.status_code)
    html = response.content.decode()
    body = re.search(r'<body>(.*)</body>', html, re.S).group(1)
    body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    body = re.sub(r'<input[^>]*name="csrfmiddlewaretoken"[^>]*>', '', body)
    pages[route] = {'title': re.search(r'<title>(.*?)</title>', html).group(1), 'html': body}
(ROOT / 'src/pages.json').write_text(json.dumps(pages))
assets = ROOT / 'public/static/studio'
assets.mkdir(parents=True, exist_ok=True)
for file in (ROOT / 'studio/static/studio').iterdir():
    if file.suffix in {'.png', '.css'} and file.name != 'studio-hero.png':
        shutil.copy2(file, assets / file.name)

shutil.copytree(ROOT / 'studio/static/studio/activities', assets / 'activities', dirs_exist_ok=True)

# The standalone preview gets the same self-contained stylesheet as Django.
index = ROOT / 'index.html'
html = index.read_text()
css = (ROOT / 'studio/static/studio/styles.css').read_text().replace('</style', '<\\/style')
style = '<style id="crew-site-styles">' + css + '</style>'
if re.search(r'<style id="crew-site-styles">.*?</style>', html, re.S):
    html = re.sub(r'<style id="crew-site-styles">.*?</style>', lambda _: style, html, flags=re.S)
else:
    html = html.replace('</head>', style + '</head>')
index.write_text(html)

media = ROOT / 'media'
if media.exists():
    shutil.copytree(media, ROOT / 'public/media', dirs_exist_ok=True)
