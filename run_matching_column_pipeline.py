import os
import re
import json
import datetime
import subprocess

WORKSPACE_DIR = "/Users/user/.gemini/antigravity/scratch/married-matching-lp"
CALENDAR_PATH = os.path.join(WORKSPACE_DIR, "editorial_calendar_matching.json")
TEMPLATE_PATH = os.path.join(WORKSPACE_DIR, "column-detail-52.html")
SITEMAP_PATH = os.path.join(WORKSPACE_DIR, "sitemap.xml")

def get_num(name):
    if name == "column-detail.html":
        return 1
    num_part = re.sub(r'\D', '', name)
    return int(num_part) if num_part else 0

def clean_html(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = " ".join(text.split())
    return text.strip()

def main():
    print("Executing automated column posting pipeline...")

    if not os.path.exists(CALENDAR_PATH):
        print(f"Error: Calendar database not found at {CALENDAR_PATH}")
        return

    with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
        calendar = json.load(f)

    # 1. Detect the next ungenerated column
    existing_files = [f for f in os.listdir(WORKSPACE_DIR) if f.startswith("column-detail") and f.endswith(".html")]
    existing_vols = {get_num(f) for f in existing_files}

    target_post = None
    for post in calendar:
        if post["vol"] not in existing_vols:
            target_post = post
            break

    if not target_post:
        print("All scheduled columns in the calendar are already generated!")
        return

    print(f"Generating Vol.{target_post['vol']}: {target_post['filename']} ({target_post['headline']})")

    # Read template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    # Dates
    today = datetime.date.today()
    period_date = today.strftime('%Y.%m.%d')
    iso_date = today.strftime('%Y-%m-%d')

    # Truncated title for breadcrumbs (20 chars max + '...')
    breadcrumb_title = target_post["headline"]
    if len(breadcrumb_title) > 20:
        breadcrumb_title = breadcrumb_title[:20] + "..."

    # Related articles
    # Let's collect metadata of existing columns to pick related ones
    existing_meta = []
    for f in os.listdir(WORKSPACE_DIR):
        if f.startswith("column-detail") and f.endswith(".html"):
            path = os.path.join(WORKSPACE_DIR, f)
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
                
                cat_match = re.search(r'<span class="article-header__category">([^<]+)</span>', content)
                date_match = re.search(r'<span class="article-header__date">([^<]+)</span>', content)
                title_match = re.search(r'<h1 class="article-header__title">([^<]+)</h1>', content)
                img_match = re.search(r'(?s)<div class="rec-article__thumb"[^>]*>\s*<img src="([^"]+)" alt="([^"]+)"', content)
                
                cat = cat_match.group(1) if cat_match else "セカンドパートナー"
                date = date_match.group(1) if date_match else "2026.06.01"
                title = title_match.group(1) if title_match else "コラム記事"
                img = img_match.group(1) if img_match else "images/column_second_partner.webp"
                alt = img_match.group(2) if img_match else ""
                
                existing_meta.append({
                    "filename": f,
                    "vol": get_num(f),
                    "category": cat,
                    "date": date,
                    "title": title,
                    "img": img,
                    "alt": alt
                })

    # Pick 2 related articles:
    # First, try to find articles in the same category as the new article (excluding itself)
    same_category_articles = [a for a in existing_meta if a["category"] == target_post["category_name"] and a["vol"] != target_post["vol"]]
    same_category_articles.sort(key=lambda x: x["vol"], reverse=True)

    related = []
    if len(same_category_articles) >= 2:
        related = same_category_articles[:2]
    else:
        related = list(same_category_articles)
        # Fill up with newest articles from other categories
        other_articles = [a for a in existing_meta if a["category"] != target_post["category_name"]]
        other_articles.sort(key=lambda x: x["vol"], reverse=True)
        needed = 2 - len(related)
        related.extend(other_articles[:needed])

    related_html = f"""                <a href="{related[0]['filename']}" class="column-card">
                  <div class="column-card__thumb">
                    <span class="column-card__badge">{related[0]['category']}</span>
                    <img src="{related[0]['img']}" alt="{related[0]['alt']}" class="column-card__img" loading="lazy">
                  </div>
                  <div class="column-card__content">
                    <div class="column-card__meta">
                      <span class="column-card__date">{related[0]['date']}</span>
                    </div>
                    <h5 class="column-card__title" style="font-size: 1.05rem;">{related[0]['title']}</h5>
                    <span class="column-card__more">記事を読む</span>
                  </div>
                </a>

                <a href="{related[1]['filename']}" class="column-card">
                  <div class="column-card__thumb">
                    <span class="column-card__badge">{related[1]['category']}</span>
                    <img src="{related[1]['img']}" alt="{related[1]['alt']}" class="column-card__img" loading="lazy">
                  </div>
                  <div class="column-card__content">
                    <div class="column-card__meta">
                      <span class="column-card__date">{related[1]['date']}</span>
                    </div>
                    <h5 class="column-card__title" style="font-size: 1.05rem;">{related[1]['title']}</h5>
                    <span class="column-card__more">記事を読む</span>
                  </div>
                </a>"""

    # Build new article body HTML
    body_html = ""
    for sec in target_post["body_sections"]:
        body_html += f"\n              <h2>{sec['h2']}</h2>\n              {sec['text']}\n"

    highlight_items = ""
    for item in target_post["highlight_box"]["items"]:
        highlight_items += f"\n                <p>{item}</p>"

    body_html += f"""
              <div class="highlight-box">
                <div class="highlight-box__title">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                  {target_post['highlight_box']['title']}
                </div>{highlight_items}
              </div>"""

    # Estimate read time (roughly 500 characters per minute)
    char_count = len(clean_html(body_html))
    read_time = max(2, int(char_count / 500))

    # Perform Replacements
    new_html = template

    # Metadata & SEO Tags
    new_html = re.sub(r'<title>.*?</title>', f'<title>{target_post["title"]}</title>', new_html)
    new_html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{target_post["description"]}">', new_html)
    new_html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{target_post["title"]}">', new_html)
    new_html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{target_post["description"]}">', new_html)
    new_html = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="https://re-en.jp/{target_post["filename"]}">', new_html)
    new_html = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://re-en.jp/{target_post["filename"]}">', new_html)

    # JSON-LD BlogPosting
    blogposting_pattern = r'(?s)<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "BlogPosting".*?</script>'
    new_blogposting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": clean_html(target_post["headline"]),
        "image": [
            f"https://re-en.jp/{target_post['banner_img']}"
        ],
        "datePublished": f"{iso_date}T09:00:00+09:00",
        "dateModified": f"{iso_date}T09:00:00+09:00",
        "author": {
            "@type": "Organization",
            "name": "Re.en 編集部",
            "url": "https://re-en.jp/"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Re.en",
            "logo": {
                "@type": "ImageObject",
                "url": "https://re-en.jp/images/favicon.png"
            }
        },
        "description": clean_html(target_post["description"])
    }
    blogposting_html = f'<script type="application/ld+json">\n  {json.dumps(new_blogposting, ensure_ascii=False, indent=2)}\n  </script>'
    new_html = re.sub(blogposting_pattern, blogposting_html, new_html)

    # JSON-LD BreadcrumbList
    breadcrumb_pattern = r'(?s)<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "BreadcrumbList".*?</script>'
    new_breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "ホーム",
                "item": "https://re-en.jp/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "コラム一覧",
                "item": "https://re-en.jp/column.html"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": breadcrumb_title,
                "item": f"https://re-en.jp/{target_post['filename']}"
            }
        ]
    }
    breadcrumb_html = f'<script type="application/ld+json">\n  {json.dumps(new_breadcrumb, ensure_ascii=False, indent=2)}\n  </script>'
    new_html = re.sub(breadcrumb_pattern, breadcrumb_html, new_html)

    # Visible Breadcrumbs (Breadcrumb Links)
    breadcrumbs_block_pattern = r'(?s)<ul class="breadcrumbs">.*?</ul>'
    breadcrumbs_block_html = f"""<ul class="breadcrumbs">
            <li class="breadcrumbs__item"><a href="index.html">ホーム</a></li>
            <li class="breadcrumbs__separator">/</li>
            <li class="breadcrumbs__item"><a href="column.html">コラム一覧</a></li>
            <li class="breadcrumbs__separator">/</li>
            <li class="breadcrumbs__item" aria-current="page" style="color: var(--color-primary);">{breadcrumb_title}</li>
          </ul>"""
    new_html = re.sub(breadcrumbs_block_pattern, breadcrumbs_block_html, new_html)

    # Visible Article Header details
    new_html = re.sub(r'<span class="article-header__category">[^<]+</span>', f'<span class="article-header__category">{target_post["category_name"]}</span>', new_html)
    new_html = re.sub(r'<span class="article-header__date">[^<]+</span>', f'<span class="article-header__date">{period_date}</span>', new_html)
    new_html = re.sub(r'<span class="article-header__readtime">読了目安: [^<]+</span>', f'<span class="article-header__readtime">読了目安: {read_time}分</span>', new_html)
    new_html = re.sub(r'<h1 class="article-header__title">[^<]+</h1>', f'<h1 class="article-header__title">{target_post["headline"]}</h1>', new_html)

    # Hero visual thumbnail image in detail page
    hero_thumb_pattern = r'(?s)<div class="rec-article__thumb"[^>]*>.*?</div>'
    hero_thumb_html = f"""<div class="rec-article__thumb" style="width: 100%; height: 350px; overflow: hidden; border-radius: 4px; margin-bottom: 32px;"><img src="{target_post['banner_img']}" alt="{target_post['headline']}" style="width: 100%; height: 100%; object-fit: cover; object-position: center 30%; opacity: 0.85; margin: 0; border: none;" loading="lazy"></div>"""
    new_html = re.sub(hero_thumb_pattern, hero_thumb_html, new_html)

    # Article Body (Safe landmark-based replacement to avoid tag mismatch)
    body_replacement_pattern = r'(?s)(<div class="article-body">).*?(?=\s*<!-- Related Articles -->)'
    new_html = re.sub(body_replacement_pattern, rf'\g<1>{body_html}\n            </div>', new_html)

    # Related articles section
    related_sec_pattern = r'(?s)(<section class="related-articles">.*?<div class="column-grid">).*?(</div>\s*</section>)'
    new_html = re.sub(related_sec_pattern, rf'\g<1>\n{related_html}\n              \g<2>', new_html)

    # Save new column detail HTML
    output_path = os.path.join(WORKSPACE_DIR, target_post["filename"])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Created details page: {target_post['filename']}")

    # 2. Recalculate Category Counts and Sync Sidebars in All Column Pages
    print("Recalculating category counts across all columns...")
    all_details = [target_post['filename']] + [f for f in os.listdir(WORKSPACE_DIR) if f.startswith("column-detail") and f.endswith(".html") and f != target_post['filename']]
    
    cat_counts = {
        "出会いのコツ": 0,
        "プライバシー対策": 0,
        "セカンドパートナー": 0,
        "お悩み": 0
    }
    
    detail_meta_list = []
    
    for f in all_details:
        path = os.path.join(WORKSPACE_DIR, f)
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
            
            cat_match = re.search(r'<span class="article-header__category">([^<]+)</span>', content)
            date_match = re.search(r'<span class="article-header__date">([^<]+)</span>', content)
            title_match = re.search(r'<h1 class="article-header__title">([^<]+)</h1>', content)
            excerpt_match = re.search(r'<meta name="description" content="([^"]+)">', content)
            img_match = re.search(r'(?s)<div class="rec-article__thumb"[^>]*>\s*<img src="([^"]+)" alt="([^"]+)"', content)
            readtime_match = re.search(r'<span class="article-header__readtime">読了目安: ([^<]+)</span>', content)
            
            cat = cat_match.group(1).strip() if cat_match else "セカンドパートナー"
            date = date_match.group(1).strip() if date_match else "2026.06.01"
            title = title_match.group(1).strip() if title_match else "コラム記事"
            excerpt = excerpt_match.group(1).strip() if excerpt_match else ""
            img = img_match.group(1).strip() if img_match else "images/column_second_partner.webp"
            alt = img_match.group(2).strip() if img_match else ""
            readtime = readtime_match.group(1).strip() if readtime_match else "2分"
            
            if cat in cat_counts:
                cat_counts[cat] += 1
            
            detail_meta_list.append({
                "filename": f,
                "vol": get_num(f),
                "category": cat,
                "date": date,
                "title": title,
                "excerpt": excerpt,
                "img": img,
                "alt": alt,
                "readtime": readtime
            })

    total_count = len(detail_meta_list)
    print(f"Total columns counted: {total_count}. Category breakdown: {cat_counts}")

    # Synchronize the sidebar Categories Widget across all column details files
    category_widget_html = f"""<div class="sidebar-widget">
              <h4 class="sidebar-widget__title">カテゴリー</h4>
              <ul class="sidebar-list">
                <li class="sidebar-list__item"><a href="column.html#全て">全てコラム <span class="sidebar-list__count">{total_count}</span></a></li>
                <li class="sidebar-list__item"><a href="column.html#出会いのコツ">出会いのコツ <span class="sidebar-list__count">{cat_counts['出会いのコツ']}</span></a></li>
                <li class="sidebar-list__item"><a href="column.html#プライバシー対策">プライバシー対策 <span class="sidebar-list__count">{cat_counts['プライバシー対策']}</span></a></li>
                <li class="sidebar-list__item"><a href="column.html#セカンドパートナー">セカンドパートナー <span class="sidebar-list__count">{cat_counts['セカンドパートナー']}</span></a></li>
                <li class="sidebar-list__item"><a href="column.html#お悩み">お悩み <span class="sidebar-list__count">{cat_counts['お悩み']}</span></a></li>
              </ul>
            </div>"""

    print("Updating sidebar category widget in all details files...")
    category_widget_pattern = r'(?s)<div class="sidebar-widget">\s*<h4 class="sidebar-widget__title">カテゴリー</h4>.*?</ul>\s*</div>'
    for f in all_details:
        path = os.path.join(WORKSPACE_DIR, f)
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        
        content = re.sub(category_widget_pattern, category_widget_html, content)
        
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

    # 3. Rebuild the Card Grid in column.html
    print("Rebuilding column.html card list and sidebar widget...")
    # Sort detail_meta_list chronologically descending by vol
    detail_meta_list.sort(key=lambda x: x["vol"], reverse=True)

    cards_html_list = []
    for meta in detail_meta_list:
        card_html = f"""              <!-- Card {meta['vol']} -->
              <!-- Card {meta['vol']} -->
              <a href="{meta['filename']}" class="column-card reveal">
                <div class="column-card__thumb">
                  <span class="column-card__badge">{meta['category']}</span>
                  <img src="{meta['img']}" alt="{meta['alt']}" class="column-card__img" loading="lazy">
                </div>
                <div class="column-card__content">
                  <div class="column-card__meta">
                    <span class="column-card__date">{meta['date']}</span>
                    <span class="column-card__readtime">読了目安: {meta['readtime']}</span>
                  </div>
                  <h3 class="column-card__title">{meta['title']}</h3>
                  <p class="column-card__excerpt">{meta['excerpt']}</p>
                  <span class="column-card__more">
                    記事を読む
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                  </span>
                </div>
              </a>"""
        cards_html_list.append(card_html)

    cards_grid_content = "\n\n".join(cards_html_list)

    # Update column.html grid and sidebar
    column_html_path = os.path.join(WORKSPACE_DIR, "column.html")
    with open(column_html_path, "r", encoding="utf-8") as file:
        column_content = file.read()

    # Replace grid
    grid_pattern = r'(?s)(<div class="column-grid">).*?(</div>\s*<!-- Pagination -->)'
    column_content = re.sub(grid_pattern, rf'\g<1>\n{cards_grid_content}\n            \g<2>', column_content)

    # Replace sidebar categories
    column_content = re.sub(category_widget_pattern, category_widget_html, column_content)

    with open(column_html_path, "w", encoding="utf-8") as file:
        file.write(column_content)
    print("Successfully updated column.html card grid and sidebar counts.")

    # 4. Rebuild sitemap.xml
    print("Rebuilding sitemap.xml...")
    if os.path.exists(SITEMAP_PATH):
        # We will parse sitemap.xml and add/update target file url element
        import xml.etree.ElementTree as ET
        import xml.dom.minidom
        
        ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")
        tree = ET.parse(SITEMAP_PATH)
        root = tree.getroot()
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Check if the url for the new file already exists
        target_loc = f"https://re-en.jp/{target_post['filename']}"
        exists = False
        for url_elem in root.findall('sm:url', ns):
            loc_elem = url_elem.find('sm:loc', ns)
            if loc_elem is not None and loc_elem.text == target_loc:
                exists = True
                lastmod_elem = url_elem.find('sm:lastmod', ns)
                if lastmod_elem is not None:
                    lastmod_elem.text = iso_date
                break
                
        if not exists:
            url_elem = ET.Element('url')
            
            loc_elem = ET.SubElement(url_elem, 'loc')
            loc_elem.text = target_loc
            
            lastmod_elem = ET.SubElement(url_elem, 'lastmod')
            lastmod_elem.text = iso_date
            
            changefreq_elem = ET.SubElement(url_elem, 'changefreq')
            changefreq_elem.text = "monthly"
            
            priority_elem = ET.SubElement(url_elem, 'priority')
            priority_elem.text = "0.7"
            
            root.append(url_elem)
            
        xml_str = ET.tostring(root, encoding='utf-8')
        parsed = xml.dom.minidom.parseString(xml_str)
        pretty_xml = parsed.toprettyxml(indent="  ")
        clean_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip()])
        
        if not clean_xml.startswith('<?xml'):
            clean_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + clean_xml
            
        with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
            f.write(clean_xml)
        print("Updated sitemap.xml successfully.")

    # 5. Trigger Vercel Production Build
    print("Triggering Vercel production deployment...")
    result = subprocess.run(["npx", "vercel", "--prod"], cwd=WORKSPACE_DIR, capture_output=True, text=True)
    print(f"Vercel Deploy Exit Code: {result.returncode}")
    print(f"Vercel Deploy Stdout:\n{result.stdout}")
    if result.returncode != 0:
        print(f"Error: Vercel deployment failed!\n{result.stderr}")
    else:
        print("Vercel deployment successfully completed.")

if __name__ == "__main__":
    main()
