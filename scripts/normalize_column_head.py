"""コラム詳細ページの <head> と周辺の整合を取る（2026-10）。

- OGP / Twitter Card / canonical / keywords / JSON-LD（BlogPosting・BreadcrumbList）を、ページの題名・説明文から作り直す
  （古い題名のまま残った重複ブロックを除く。og:url は .html なし）
- パンくず・ヒーロー画像の alt を、現在のH1に合わせる
- 「おすすめの記事」（サイドバー）と「関連記事」を、同じカテゴリ・近いテーマの記事に差し替える
何度実行しても同じ結果になる。run_matching_column_pipeline.py の末尾からも呼ぶ。
"""
import datetime
import glob
import html as htmllib
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://re-en.jp"
PILLARS = [17, 112, 54, 114]  # おすすめの記事（サイドバー）に常に出す
TODAY = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y-%m-%d")


def num(f):
    m = re.search(r"column-detail-(\d+)\.html$", f)
    return int(m.group(1)) if m else None


def esc(t):
    return htmllib.escape(t, quote=True)


def load_pages():
    pages = {}
    for f in glob.glob(os.path.join(ROOT, "column-detail-*.html")):
        n = num(f)
        if n is None:
            continue
        s = open(f, encoding="utf-8").read()
        g = lambda p: (re.search(p, s, re.S).group(1) if re.search(p, s, re.S) else "")
        body = g(r'<div class="article-body">(.*?)<!-- Related')
        pages[n] = {
            "file": f, "s": s,
            "title": htmllib.unescape(g(r"<title>(.*?)</title>")),
            "desc": htmllib.unescape(g(r'<meta name="description" content="([^"]*)"')),
            "h1": htmllib.unescape(g(r'<h1 class="article-header__title">([^<]*)</h1>')),
            "cat": g(r'<span class="article-header__category">([^<]+)</span>'),
            "date": g(r'<span class="article-header__date">([^<]+)</span>'),
            "img": g(r'<div class="article-hero-thumb"[^>]*><img src="([^"]+)"'),
            "words": set(re.findall(r"[一-龠ァ-ヶー]{2,}", re.sub(r"<[^>]+>", "", g(r'<h1 class="article-header__title">([^<]*)</h1>') + " " + "".join(re.findall(r"<h[23][^>]*>(.*?)</h[23]>", body))))),
        }
    return pages


def og_image(img):
    stem = os.path.splitext(os.path.basename(img or ""))[0]
    if stem and os.path.exists(os.path.join(ROOT, "images", "og", stem + ".jpg")):
        return f"{BASE}/images/og/{stem}.jpg"
    return f"{BASE}/{img}" if img else f"{BASE}/images/og/hero_lifestyle.jpg"


def jsonld(obj):
    return '<script type="application/ld+json">\n  ' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n  </script>"


def related_for(n, pages):
    me = pages[n]
    scored = []
    for m, p in pages.items():
        if m == n:
            continue
        sc = len(me["words"] & p["words"]) + (3 if p["cat"] == me["cat"] else 0)
        scored.append((-sc, abs(m - n), m))
    scored.sort()
    return [m for _, _, m in scored[:3]]


def card(m, pages):
    p = pages[m]
    return f'''                <a href="/column-detail-{m}" class="column-card">
                  <div class="column-card__thumb">
                    <span class="column-card__badge">{esc(p["cat"])}</span>
                    <img src="{esc(p["img"])}" alt="{esc(p["h1"])}" class="column-card__img" loading="lazy">
                  </div>
                  <div class="column-card__content">
                    <div class="column-card__meta">
                      <span class="column-card__date">{p["date"]}</span>
                    </div>
                    <h5 class="column-card__title" style="font-size: 1.05rem;">{esc(p["h1"])}</h5>
                    <span class="column-card__more">記事を読む</span>
                  </div>
                </a>'''


def rec_widget(pages):
    items = ""
    for m in PILLARS:
        if m in pages:
            p = pages[m]
            items += f'''
                <a href="column-detail-{m}" class="rec-article">
                  <div class="rec-article__content">
                    <h5 class="rec-article__title">{esc(p["h1"])}</h5>
                    <span class="rec-article__date">{p["date"]}</span>
                  </div>
                </a>
'''
    return f'''<div class="sidebar-widget">
              <h4 class="sidebar-widget__title">おすすめの記事</h4>
              <div class="sidebar-list">{items}              </div>
            </div>'''


def fix(n, pages, cal):
    p = pages[n]
    s = p["s"]
    title, desc, h1 = p["title"], p["desc"], p["h1"]
    url = f"{BASE}/column-detail-{n}"
    img = og_image(p["img"])
    kw = (cal.get(f"column-detail-{n}.html") or {}).get("keywords", "")
    # 1. 既存のOGP/Twitter/canonical/keywords/コメントを外す
    s = re.sub(r'\s*<meta property="og:[^"]*" content="[^"]*">', "", s)
    s = re.sub(r'\s*<meta name="twitter:[^"]*" content="[^"]*">', "", s)
    s = re.sub(r'\s*<link rel="canonical"[^>]*>', "", s)
    s = re.sub(r'\s*<meta name="keywords"[^>]*>', "", s)
    s = re.sub(r"\s*<!-- (OG Tags|OGP & Social Meta Tags) -->", "", s)
    block = [f'<link rel="canonical" href="{url}">']
    if kw:
        block.append(f'<meta name="keywords" content="{esc(kw)}">')
    block += [
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        '<meta property="og:type" content="article">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{img}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:site_name" content="Re.en（リエン）">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
        f'<meta name="twitter:image" content="{img}">',
    ]
    s = re.sub(r"(</title>)", lambda m: m.group(1) + "\n  <!-- OGP & Social Meta Tags -->\n  " + "\n  ".join(block), s, count=1)
    # 2. JSON-LD: BlogPosting と BreadcrumbList を作り直す（重複を除く）
    def ld_type(t):
        return re.search(r'"@type":\s*"(\w+)"', t).group(1) if re.search(r'"@type":\s*"(\w+)"', t) else ""
    scripts = re.findall(r'\s*<script type="application/ld\+json">.*?</script>', s, re.S)
    old_blog = next((x for x in scripts if ld_type(x) == "BlogPosting"), "")
    pub = re.search(r'"datePublished":\s*"([^"]+)"', old_blog)
    pub = pub.group(1) if pub else f"{TODAY}T09:00:00+09:00"
    for x in scripts:
        if ld_type(x) in ("BlogPosting", "BreadcrumbList"):
            s = s.replace(x, "", 1)
    blog = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": h1,
            "image": [img], "datePublished": pub, "dateModified": f"{TODAY}T09:00:00+09:00",
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "author": {"@type": "Organization", "name": "Re.en 編集部", "url": f"{BASE}/"},
            "publisher": {"@type": "Organization", "name": "Re.en",
                          "logo": {"@type": "ImageObject", "url": f"{BASE}/images/favicon.png"}},
            "description": desc}
    crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "ホーム", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": "コラム一覧", "item": f"{BASE}/column"},
        {"@type": "ListItem", "position": 3, "name": h1, "item": url}]}
    s = s.replace("</head>", "  " + jsonld(blog) + "\n  " + jsonld(crumb) + "\n</head>", 1)
    # 3. パンくず・ヒーロー画像alt
    s = re.sub(r'(<li class="breadcrumbs__item" aria-current="page"[^>]*>)[^<]*(</li>)', lambda m: m.group(1) + esc(h1) + m.group(2), s, count=1)
    s = re.sub(r'(<header class="article-header">.*?<img [^>]*?alt=")[^"]*(")', lambda m: m.group(1) + esc(h1) + m.group(2), s, count=1, flags=re.S)
    # 4. 関連記事・おすすめ
    rel = "\n\n".join(card(m, pages) for m in related_for(n, pages))
    s = re.sub(r'(<section class="related-articles">\s*<h4 class="related-articles__title">関連記事</h4>\s*<div class="column-grid">).*?(</div>\s*</section>)',
               lambda m: m.group(1) + "\n" + rel + "\n              " + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'<div class="sidebar-widget">\s*<h4 class="sidebar-widget__title">おすすめの記事</h4>.*?</div>\s*</div>',
               lambda m: rec_widget(pages), s, count=1, flags=re.S)
    if s != p["s"]:
        open(p["file"], "w", encoding="utf-8").write(s)
    return s != p["s"]


def main():
    cal = {}
    cp = os.path.join(ROOT, "editorial_calendar_matching.json")
    if os.path.exists(cp):
        cal = {c["filename"]: c for c in json.load(open(cp, encoding="utf-8"))}
    pages = load_pages()
    changed = sum(fix(n, pages, cal) for n in sorted(pages))
    print(f"normalize_column_head: {len(pages)}本中{changed}本を更新")


if __name__ == "__main__":
    main()
