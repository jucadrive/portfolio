"""Regenerate static HTML and original SVG diagrams using only content.json."""
from pathlib import Path
from html import escape
import json
import argparse

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
PROFILE = DATA['profile']
PROJECTS = DATA['projects']

def e(value):
    return escape(str(value), quote=True)

def write(path, text):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')

def header(prefix='', detail=False):
    links = [('journey','경험'),('work','프로젝트'),('stack','기술'),('credentials','교육·자격'),('contact','연락처')]
    home = prefix + 'index.html'
    nav = ''.join(f'<a href="{home}#{id}">{label}</a>' for id,label in links)
    return f'''<a class="skip" href="#main">본문으로 건너뛰기</a>
<header class="site-header"><div class="header-inner">
<a class="brand" href="{home}" aria-label="{e(PROFILE['name'])} 포트폴리오 홈"><span class="brand-dot"></span>{e(PROFILE['name'])}<span class="brand-sub">BACKEND PORTFOLIO</span></a>
<button class="menu-toggle" type="button" aria-label="메뉴 열기" aria-expanded="false" aria-controls="main-nav">메뉴 <span aria-hidden="true">☰</span></button>
<nav id="main-nav" aria-label="주 메뉴">{nav}</nav></div></header>'''

def footer(prefix=''):
    return f'''<footer><div class="container footer-inner"><p>© 2026 {e(PROFILE['name'])} <span>· Backend Portfolio</span></p><a href="{prefix}index.html#contact">연락처 ↗</a></div></footer>
<a class="to-top" href="#top" aria-label="맨 위로">↑</a>'''

def shell(title, description, body, prefix=''):
    return f'''<!doctype html>
<html lang="ko" class="{'project-page' if prefix else 'home-page'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(description)}"><meta name="theme-color" content="#23273f">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website">
<title>{e(title)}</title><link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg">
<link rel="stylesheet" href="{prefix}assets/style.css"><script src="{prefix}assets/main.js" defer></script></head>
<body id="top">{body}</body></html>'''

def chips(items):
    return '<ul class="tags" aria-label="사용 기술">'+''.join(f'<li>{e(t)}</li>' for t in items)+'</ul>'

def eyebrow(label):
    return f'<p class="eyebrow">{e(label)}</p>'

def section_head(number, label, title, intro=''):
    return f'{eyebrow(number+" / "+label)}<h2>{e(title)}</h2>'+ (f'<p class="section-intro">{e(intro)}</p>' if intro else '')

def make_svg(path, title, nodes, theme, branch=None):
    palette = {'violet':('#6653be','#f0edf9'), 'blue':('#32679b','#edf3f9'), 'green':('#347768','#edf5f1'), 'amber':('#946b35','#f9f2e9')}
    color,bg = palette[theme]
    height = 380 if branch else 260
    boxes = []
    for i,(label,caption) in enumerate(nodes):
        x = 30+i*280
        boxes.append(f'''<g><rect x="{x}" y="78" width="250" height="116" rx="12" fill="white" stroke="{color}" stroke-opacity=".28"/>
<text x="{x+20}" y="104" fill="{color}" font-size="13" letter-spacing="1.5">0{i+1}</text>
<text x="{x+20}" y="138" fill="#23273f" font-size="22" font-weight="700">{e(label)}</text>
<text x="{x+20}" y="168" fill="#556173" font-size="17">{e(caption)}</text></g>''')
        if i < len(nodes)-1:
            boxes.append(f'<path d="M {x+251} 136 H {x+276}" stroke="{color}" stroke-width="2" marker-end="url(#arrow)"/>')
    if branch:
        boxes.append(f'<text x="30" y="248" font-size="14" fill="{color}">별도 처리 경로</text>')
        for i,(label,caption) in enumerate(branch):
            x = 30+i*560
            boxes.append(f'<rect x="{x}" y="263" width="530" height="76" rx="10" fill="white" stroke="{color}" stroke-opacity=".28"/><text x="{x+20}" y="294" fill="#23273f" font-size="20" font-weight="700">{e(label)}</text><text x="{x+20}" y="321" fill="#556173" font-size="17">{e(caption)}</text>')
        boxes.append(f'<path d="M 562 301 H 586" stroke="{color}" stroke-width="2" marker-end="url(#arrow)"/>')
    desc = ' → '.join(f'{a}: {b}' for a,b in nodes)
    if branch:
        desc += '; 별도 경로: '+' → '.join(f'{a}: {b}' for a,b in branch)
    write(path, f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1150 {height}" width="1150" height="{height}" role="img" aria-labelledby="title desc">
<title id="title">{e(title)}</title><desc id="desc">{e(desc)}</desc><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="{color}"/></marker></defs>
<rect width="1150" height="{height}" rx="18" fill="{bg}"/><text x="30" y="41" fill="{color}" font-family="sans-serif" font-size="14" letter-spacing="2">{e(title)}</text><g font-family="'Malgun Gothic', sans-serif">{''.join(boxes)}</g></svg>''')

def diagram(src, title, note, steps=None):
    step_text = ''
    if steps:
        step_text = '<ol class="flow-text">'+''.join(f'<li><strong>{e(a)}</strong><span>{e(b)}</span></li>' for a,b in steps)+'</ol>'
    caption = f'<figcaption>{e(note)}</figcaption>' if note else ''
    return f'''<figure class="diagram"><div class="figure-heading"><h3>{e(title)}</h3><button type="button" class="zoom-link" data-zoom="{src}" data-title="{e(title)}">도식 확대 <span aria-hidden="true">↗</span></button></div>
<button class="diagram-open" type="button" data-zoom="{src}" data-title="{e(title)}" aria-label="{e(title)} 도식 확대"><img src="{src}" alt="{e(title)}" loading="lazy" width="1150" height="260"></button>{step_text}{caption}</figure>'''

def modal():
    return '''<dialog id="diagram-dialog" aria-labelledby="diagram-title"><div class="dialog-heading"><h2 id="diagram-title">처리 흐름</h2><button type="button" id="dialog-close" aria-label="확대 도식 닫기">닫기 ×</button></div><div class="zoom-toolbar" aria-label="도식 확대 도구"><button type="button" id="zoom-out" aria-label="도식 축소">−</button><output id="zoom-level" aria-live="polite">100%</output><button type="button" id="zoom-in" aria-label="도식 확대">+</button><button type="button" id="zoom-reset">크기 초기화</button><span>확대 후 가로·세로로 스크롤할 수 있습니다.</span></div><div class="zoom-canvas"><img id="zoom-image" alt="선택한 확대 도식" draggable="false"></div></dialog>'''

def make_home():
    timeline = ''.join(f'''<li><p class="timeline-date"><span>{t['number']}</span>{e(t['date'])}</p><h2>{e(t['title'])}</h2><p>{e(t['text'])}</p><a href="{t['link']}">{e(t['label'])} <span aria-hidden="true">↗</span></a></li>''' for t in PROFILE['timeline'])
    cards=[]
    for p in PROJECTS:
        cards.append(f'''<a class="project-card theme-{p['theme']}" href="projects/{p['id']}.html" aria-label="{e(p['title'])} 상세 보기"><div class="card-top"><span>CASE {p['number']} · {p['kind']}</span><span class="status status-{p['statusType']}">{e(p['status'])}</span></div>
<div class="card-art"><img src="assets/{p['id']}-overview.svg" alt="{e(p['cardFlow'])}" width="1150" height="260" loading="lazy"></div><div class="card-body"><h3>{e(p['title'])}</h3><p class="card-flow">{e(p['cardFlow'])}</p><p>{e(p['summary'])}</p><dl><div><dt>개발 내용</dt><dd>{e(p['cardRole'])}</dd></div><div><dt>설계</dt><dd>{e(p['cardDesign'])}</dd></div></dl>{chips(p['tags'][:4])}<div class="card-link">프로젝트 상세 보기 <span aria-hidden="true">↗</span></div></div></a>''')
    stacks = ''.join(f'<article class="stack-card">{eyebrow(s["label"])}<h3>{e(s["title"])}</h3>{chips(s["items"])}<p>{e(s["text"])}</p></article>' for s in PROFILE['stack'])
    def credentials(items):
        return '<ul class="credential-list">'+''.join(f'<li><span>{e(x["date"])}</span><div><h4>{e(x["title"])}</h4><p>{e(x["text"])}</p></div></li>' for x in items)+'</ul>'
    hero_title='<br>'.join(e(x) for x in PROFILE['headline'])
    body = header()+f'''<main id="main"><section class="hero" aria-labelledby="hero-title"><div class="container"><div class="hero-top"><div><p class="eyebrow">JU HYUNJUN / BACKEND PORTFOLIO</p><h1 id="hero-title">{hero_title}</h1><p class="hero-intro">{e(PROFILE['intro'])}</p><a class="primary-button" href="#work">프로젝트 살펴보기 <span aria-hidden="true">↘</span></a></div><aside class="hero-aside"><span class="small-label">BACKEND EXPERIENCE</span><p>API 개발<br>데이터 처리<br>성능 개선</p><span class="aside-bottom">Java · Kotlin · Spring Boot</span></aside></div>
<div id="journey" class="timeline-wrap"><p class="small-label">EXPERIENCE & PROJECTS</p><ol class="timeline">{timeline}</ol><p class="hero-footnote">{e(PROFILE['experience'])}</p></div></div></section>
<section class="section container" id="work">{section_head('01','SELECTED PROJECTS','실무 및 개인 프로젝트','배송 시스템 연계 API, 등산 기록 서비스와 재고 할당 시스템의 개발 경험을 소개합니다.')}<div class="project-grid">{''.join(cards)}</div></section>
<section class="section stack-section" id="stack"><div class="container">{section_head('02','TECH STACK','기술 역량','API 개발부터 데이터 조회·저장, 배포와 성능 분석까지 경험한 기술입니다.')}<div class="stack-grid">{stacks}</div></div></section>
<section class="section container" id="credentials">{section_head('03','EDUCATION & CERTIFICATIONS','교육 및 자격')}<div class="credentials-grid"><article><h3>교육·학력</h3>{credentials(PROFILE['education'])}</article><article><h3>자격</h3>{credentials(PROFILE['certifications'])}</article></div></section>
<section class="section contact-section" id="contact"><div class="container contact-inner"><div>{eyebrow('04 / CONTACT')}<h2>함께 풀어갈 문제를<br>이야기하고 싶습니다.</h2><p>요구사항을 데이터와 API로 구체화하고, 운영 중 발생하는 문제를 개선하는 개발을 지향합니다. 새로운 환경에서도 꾸준히 배우며 함께 성장하고 싶습니다.</p></div><div class="contact-card"><span class="small-label">EMAIL</span><a href="mailto:{e(PROFILE['email'])}">{e(PROFILE['email'])} <span aria-hidden="true">↗</span></a><p>{e(PROFILE['name'])} · {e(PROFILE['role'])}</p></div></div></section></main>'''+footer()
    write('index.html',shell(PROFILE['name']+' | Backend Portfolio',PROFILE['intro'],body))

def make_detail(p):
    prefix='../'
    a=p['architecture']
    nav=''.join(f'<a href="#{id}">{label}</a>' for id,label in [('overview','개요'),('architecture','아키텍처'),('features','기능별 구현'),('verification','결과·테스트'),('reflection','회고')])
    metrics=''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k,v in p['metrics'])
    buttons=[]; panels=[]
    for i,f in enumerate(p['features']):
        buttons.append(f'<button id="tab-{f["id"]}" type="button" role="tab" aria-selected="{str(i==0).lower()}" aria-controls="panel-{f["id"]}" tabindex="{0 if i==0 else -1}"><span class="tab-index">0{i+1}</span>{e(f["title"])}<span aria-hidden="true" class="tab-arrow">→</span></button>')
        decisions=''.join(f'<article class="decision"><h4>{e(t)}</h4><p>{e(d)}</p></article>' for t,d in f['decisions'])
        panels.append(f'''<article class="feature-panel" role="tabpanel" id="panel-{f['id']}" aria-labelledby="tab-{f['id']}" tabindex="0"><p class="eyebrow">FEATURE 0{i+1} <span class="feature-state">{e(f['status'])}</span></p><h3 class="feature-title">{e(f['title'])}</h3><p class="feature-intro">{e(f['intro'])}</p>
{diagram(prefix+'assets/'+p['id']+'-'+f['id']+'.svg',f['title']+' 처리 흐름',f.get('flowNote',''),f['flow'])}
<div class="problem-solution"><article><span class="small-label">PROBLEM</span><h4>문제</h4><p>{e(f['problem'])}</p></article><article><span class="small-label">SOLUTION</span><h4>해결</h4><p>{e(f['solution'])}</p></article></div>
<h4 class="feature-subtitle">설계 이유와 트레이드오프</h4>{decisions}<div class="validation-note"><span class="small-label">VALIDATION</span><h4>구현 결과와 테스트</h4><p>{e(f['validation'])}</p></div></article>''')
    repo=f'<a class="secondary-button" href="{e(p["repository"])}" target="_blank" rel="noopener noreferrer">GitHub 저장소 ↗</a>' if p.get('repository') else ''
    rows=''.join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k,v in p['verification'])
    other_links=''.join(f'<a href="{x["id"]}.html"><span>{x["kind"]}</span><strong>{e(x["title"])}</strong><span aria-hidden="true">↗</span></a>' for x in PROJECTS if x['id']!=p['id'])
    body=header(prefix,True)+f'''<main id="main" class="detail theme-{p['theme']}"><div class="container"><div class="breadcrumb"><a href="../index.html#work">← 전체 프로젝트</a><span>CASE {p['number']} / {p['kind']}</span></div><section class="detail-hero" id="overview">{eyebrow('PROJECT DETAIL / '+p['kind'])}<h1>{e(p['title'])}</h1><p class="detail-subtitle">{e(p['subtitle'])}</p><p class="project-meta"><span>{e(p['period'])}</span><span class="status status-{p['statusType']}">{e(p['status'])}</span></p>{chips(p['tags'])}
<div class="snapshot"><div><span class="small-label">OVERVIEW</span><h2>프로젝트 개요</h2><p>{e(p['summary'])}</p></div><div><span class="small-label">SCOPE</span><h2>담당 업무 및 개발 내용</h2><p>{e(p['scope'])}</p></div></div><dl class="metrics">{metrics}</dl>{repo}</section></div>
<nav class="detail-nav" aria-label="프로젝트 목차"><div class="container">{nav}</div></nav>
<div class="container"><section class="detail-section" id="architecture">{section_head('01','ARCHITECTURE','시스템 구성과 처리 흐름')}{diagram(prefix+'assets/'+p['id']+'-overview.svg',a['title'],a['note'],a['nodes'])}</section>
<section class="detail-section" id="features">{section_head('02','IMPLEMENTATION','주요 기능과 설계','기능별 처리 흐름과 문제 해결 과정, 설계 이유와 구현 결과를 소개합니다.')}<noscript><p class="notice">JavaScript가 꺼져 있어 모든 기능 설명을 순서대로 표시합니다. 도식은 이미지 파일을 직접 열어 볼 수 있습니다.</p></noscript><div class="features-layout"><aside class="feature-nav"><p class="small-label">FEATURES</p><div role="tablist" aria-label="{e(p['title'])} 기능" aria-orientation="vertical">{''.join(buttons)}</div><a class="back-home" href="../index.html#work">← 프로젝트 목록</a></aside><div class="feature-content">{''.join(panels)}</div></div></section>
<section class="detail-section" id="verification">{section_head('03','RESULTS & TESTING','개발 결과와 테스트')}<div class="table-wrap"><table><caption>{e(p['title'])} 개발 결과</caption><thead><tr><th scope="col">항목</th><th scope="col">결과</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section class="detail-section" id="reflection">{section_head('04','REFLECTION','개발 회고와 개선 방향')}<div class="reflection-grid"><article><h3>회고</h3><p>{e(p['reflection'])}</p></article><article><span class="small-label">NEXT / 향후 계획</span><h3>향후 개선 방향</h3><p>{e(p['next'])}</p></article></div></section>
<section class="other-projects"><h2>다른 프로젝트도 살펴보기</h2><div>{other_links}</div><a class="secondary-button" href="../index.html#work">전체 프로젝트로 돌아가기 ←</a></section></div></main>'''+modal()+footer(prefix)
    write('projects/'+p['id']+'.html',shell(p['title']+' | '+PROFILE['name'],p['subtitle'],body,prefix))

def build(base_path='/'):
    for p in PROJECTS:
        a=p['architecture']
        make_svg('assets/'+p['id']+'-overview.svg',a['title'],a['nodes'],p['theme'],a.get('branch'))
        for f in p['features']:
            make_svg('assets/'+p['id']+'-'+f['id']+'.svg',f['title']+' 처리 흐름',f['flow'],p['theme'])
        make_detail(p)
    make_home()
    write('.nojekyll','')
    # Inline page is independent of the missing URL depth on GitHub Pages.
    home_url = '/' + base_path.strip('/') + '/' if base_path.strip('/') else '/'
    write('404.html','''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>페이지를 찾을 수 없습니다</title><style>body{margin:0;background:#f7f6f2;color:#23273f;font-family:sans-serif;display:grid;min-height:100vh;place-items:center}main{padding:30px;max-width:600px}h1{font-size:32px}a,button{color:#6653be;font-size:16px;margin-right:16px}button{background:none;border:0;cursor:pointer}</style></head><body><main><p>404 / PAGE NOT FOUND</p><h1>페이지를 찾을 수 없습니다.</h1><p>주소를確認하거나 포트폴리오 홈으로 이동해 주세요.</p><a id="home" href="HOME_URL">홈으로 이동 →</a><button id="back" type="button">이전 페이지</button></main><script>document.getElementById('back').addEventListener('click',()=>history.back());</script></body></html>'''.replace('HOME_URL',e(home_url)).replace('確認','확인'))
    print(f'Generated home, {len(PROJECTS)} project pages, 404 and {sum(1+len(p["features"]) for p in PROJECTS)} original diagrams.')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-path',default='/')
    build(parser.parse_args().base_path)
