"""Check generated pages, relative links, diagrams and public-file hygiene."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
errors=[]
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=[]; self.links=[]; self.tabs=[]; self.panels=[]; self.roles=[]; self.h1=0; self.images=0
        self.feed(text)
    def handle_starttag(self,tag,attributes):
        a=dict(attributes)
        if a.get('id'):self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        for key in ['href','src']:
            if a.get(key):self.links.append(a[key])
        if a.get('data-zoom'):self.links.append(a['data-zoom'])
        if tag=='img':
            self.images+=1
            if not a.get('alt'):errors.append('Image missing alternative text')
        if a.get('role')=='tab':self.tabs.append(a)
        if a.get('role')=='tabpanel':self.panels.append(a)

pages={f:Page(f.read_text(encoding='utf-8')) for f in ROOT.rglob('*.html') if '.local' not in f.parts and '_public' not in f.parts}
for file,page in pages.items():
    relative=file.relative_to(ROOT)
    if page.h1!=1:errors.append(f'{relative}: expected one h1')
    if len(page.ids)!=len(set(page.ids)):errors.append(f'{relative}: duplicate ids')
    for link in page.links:
        url=urlsplit(link)
        if url.scheme in ('https','mailto','data'):continue
        if url.scheme or url.netloc:errors.append(f'{relative}: unexpected external URL');continue
        if url.path.startswith('/') and file.name=='404.html':continue
        target=(file.parent/unquote(url.path)).resolve() if url.path else file
        if not target.is_relative_to(ROOT):errors.append(f'{relative}: path leaves site');continue
        if target.is_dir():target=target/'index.html'
        if not target.exists():errors.append(f'{relative}: missing {link}')
        if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{relative}: missing anchor {link}')
    if page.tabs:
        if len(page.tabs)!=len(page.panels):errors.append(f'{relative}: tab/panel mismatch')
        if sum(t.get('aria-selected')=='true' for t in page.tabs)!=1:errors.append(f'{relative}: selected tab mismatch')
        for tab in page.tabs:
            pane=next((p for p in page.panels if p['id']==tab['aria-controls']),None)
            if not pane or pane['aria-labelledby']!=tab['id']:errors.append(f'{relative}: invalid ARIA tab wiring')

content=json.loads((ROOT/'content.json').read_text(encoding='utf-8'))
for p in content['projects']:
    if p['kind']=='업무 프로젝트' and p.get('repository'):errors.append('Work project has repository URL')
    if p.get('repository') and p['repository']!='https://github.com/jucadrive/HomeLab':errors.append('Repository URL is outside supplied allowlist')
for svg in (ROOT/'assets').glob('*.svg'):
    try: ET.parse(svg)
    except ET.ParseError:errors.append(f'{svg.name}: invalid SVG')

patterns=[
    (r'(?i)[a-z]:[\\/](?:Users|dev|workspace|tmp)[\\/]','local absolute path'),
    (r'(?i)(?:file://|https?://(?:10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.))','private address'),
    (r'(?i)(?:AKIA|ASIA)[A-Z0-9]{16}|ghp_[A-Za-z0-9]{25,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----','credential signature'),
    (r'(?i)(?:jdbc:|postgres(?:ql)?://|mysql://)','database connection URL'),
]
allowed_suffixes={'.html','.css','.js','.json','.svg','.md','.py','.yml','.gitignore',''}
for f in ROOT.rglob('*'):
    if not f.is_file() or any(part in ('.local','__pycache__','_public','.git') for part in f.relative_to(ROOT).parts):continue
    if f.is_symlink():errors.append('Symlink in site');continue
    if f.suffix not in allowed_suffixes and f.name!='.gitignore':errors.append(f'Unexpected publish candidate: {f.name}')
    if f.suffix in {'.pdf','.doc','.docx','.env','.csv','.sql','.log'}:errors.append(f'Raw or runtime data: {f.name}')
    text=f.read_text(encoding='utf-8')
    # This checker contains the detection expressions themselves, not source data.
    if f.resolve()==Path(__file__).resolve():continue
    for pattern,label in patterns:
        if re.search(pattern,text):errors.append(f'{f.relative_to(ROOT)}: {label}')
print(f'Checked {len(pages)} HTML pages, {len(list((ROOT/"assets").glob("*.svg")))} SVGs, links, anchors, ARIA and file hygiene.')
if errors:
    print('\n'.join(errors));sys.exit(1)
print('PASS: all static checks passed. Human content review remains separate.')
