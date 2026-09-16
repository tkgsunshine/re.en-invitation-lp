import os
import re
import json
import datetime

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
CALENDAR_PATH = os.path.join(WORKSPACE_DIR, "editorial_calendar_matching.json")
SITEMAP_PATH = os.path.join(WORKSPACE_DIR, "sitemap.xml")

def get_num(name):
    if name == "column-detail.html":
        return 1
    num_part = re.sub(r'\D', '', name)
    return int(num_part) if num_part else 0

def main():
    print("Running rebuild_matching_blog_index.py (Clean URL & Photo Mode)...")

    # Load calendar if available for image lookup fallback
    calendar_map = {}
    if os.path.exists(CALENDAR_PATH):
        with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
            cal_data = json.load(f)
            for item in cal_data:
                calendar_map[item["filename"]] = item

    all_details = [f for f in os.listdir(WORKSPACE_DIR) if f.startswith("column-detail") and f.endswith(".html")]
    
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
            readtime_match = re.search(r'<span class="article-header__readtime">読了目安: ([^<]+)</span>', content)
            
            cat = cat_match.group(1).strip() if cat_match else "セカンドパートナー"
            date = date_match.group(1).strip() if date_match else "2026.06.01"
            title = title_match.group(1).strip() if title_match else "コラム記事"
            excerpt = excerpt_match.group(1).strip() if excerpt_match else ""
            readtime = readtime_match.group(1).strip() if readtime_match else "7分"
            
            # Photo image extraction
            img_path = "images/column_second_partner.webp"
            img_match = re.search(r'<div class="rec-article__thumb"[^>]*>\s*<img src="([^"]+)"', content)
            if img_match:
                img_path = img_match.group(1).strip()
            elif f in calendar_map and "banner_img" in calendar_map[f]:
                img_path = calendar_map[f]["banner_img"]
            
            if cat in cat_counts:
                cat_counts[cat] += 1
            
            detail_meta_list.append({
                "filename": f,
                "clean_url": f.replace('.html', ''),
                "vol": get_num(f),
                "category": cat,
                "date": date,
                "title": title,
                "excerpt": excerpt,
                "img_path": img_path,
                "readtime": readtime
            })

    total_count = len(detail_meta_list)
    print(f"Total columns counted: {total_count}. Category breakdown: {cat_counts}")

    # Synchronize sidebar Categories Widget across all column details files
    category_widget_html = f"""<div class="sidebar-widget">
              <h4 class="sidebar-widget__title">カテゴリー</h4>
              <ul class="sidebar-list">
                <li class="sidebar-list__item"><a href="column#全て">全てコラム <span class="sidebar-list__count">{total_count}</span></a></li>
                <li class="sidebar-list__item"><a href="column#出会いのコツ">出会いのコツ <span class="sidebar-list__count">{cat_counts['出会いのコツ']}</span></a></li>
                <li class="sidebar-list__item"><a href="column#プライバシー対策">プライバシー対策 <span class="sidebar-list__count">{cat_counts['プライバシー対策']}</span></a></li>
                <li class="sidebar-list__item"><a href="column#セカンドパートナー">セカンドパートナー <span class="sidebar-list__count">{cat_counts['セカンドパートナー']}</span></a></li>
                <li class="sidebar-list__item"><a href="column#お悩み">お悩み <span class="sidebar-list__count">{cat_counts['お悩み']}</span></a></li>
              </ul>
            </div>"""

    recommended_widget_html = """<div class="sidebar-widget">
              <h4 class="sidebar-widget__title">おすすめの記事</h4>
              <div class="sidebar-list" style="gap: 20px;">
                <a href="column-detail" class="rec-article">
                  <div class="rec-article__thumb">
                    <img src="images/column_second_partner.webp" alt="セカンドパートナーとは？既婚者ならではの新しい関係の形" class="rec-article__img" loading="lazy" width="70" height="70">
                  </div>
                  <div class="rec-article__content">
                    <h5 class="rec-article__title">セカンドパートナーとは？既婚者ならではの新しい関係の形</h5>
                    <span class="rec-article__date">2026.06.15</span>
                  </div>
                </a>

                <a href="column-detail-2" class="rec-article">
                  <div class="rec-article__thumb">
                    <img src="images/column_privacy.webp" alt="既婚者マッチングで絶対に身内にバレないための対策5選" class="rec-article__img" loading="lazy" width="70" height="70">
                  </div>
                  <div class="rec-article__content">
                    <h5 class="rec-article__title">既婚者マッチングで絶対に身内にバレないための対策5選</h5>
                    <span class="rec-article__date">2026.06.12</span>
                  </div>
                </a>

                <a href="column-detail-3" class="rec-article">
                  <div class="rec-article__thumb">
                    <img src="images/column_profile.webp" alt="セカンドパートナー探しで失敗しないプロフィールの書き方" class="rec-article__img" loading="lazy" width="70" height="70">
                  </div>
                  <div class="rec-article__content">
                    <h5 class="rec-article__title">セカンドパートナー探しで失敗しないプロフィールの書き方</h5>
                    <span class="rec-article__date">2026.06.10</span>
                  </div>
                </a>
              </div>
            </div>"""

    print("Updating sidebar widgets and header thumbs in all details files...")
    category_widget_pattern = r'(?s)<div class="sidebar-widget">\s*<h4 class="sidebar-widget__title">カテゴリー</h4>.*?</ul>\s*</div>'
    recommended_widget_pattern = r'(?s)<div class="sidebar-widget">\s*<h4 class="sidebar-widget__title">おすすめの記事</h4>.*?</div>\s*</div>'
    header_thumb_pattern = r'(?s)(<header class="article-header">.*?<h1 class="article-header__title">[^<]+</h1>\s*)<div class="rec-article__thumb"'

    for f in all_details:
        path = os.path.join(WORKSPACE_DIR, f)
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        
        content = re.sub(category_widget_pattern, category_widget_html, content)
        content = re.sub(recommended_widget_pattern, recommended_widget_html, content)
        content = re.sub(header_thumb_pattern, r'\g<1><div class="article-hero-thumb"', content)
        
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

    # Rebuild the Card Grid in column.html
    print("Rebuilding column.html card list and sidebar widget...")
    detail_meta_list.sort(key=lambda x: x["vol"], reverse=True)

    cards_html_list = []
    for meta in detail_meta_list:
        card_html = f"""              <!-- Card {meta['vol']} -->
              <a href="{meta['clean_url']}" class="column-card reveal">
                <div class="column-card__thumb">
                  <span class="column-card__badge">{meta['category']}</span>
                  <img src="{meta['img_path']}" alt="{meta['title']}" class="column-card__img" loading="lazy" width="400" height="250">
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

    # Replace sidebar categories and recommended articles
    column_content = re.sub(category_widget_pattern, category_widget_html, column_content)
    column_content = re.sub(recommended_widget_pattern, recommended_widget_html, column_content)

    with open(column_html_path, "w", encoding="utf-8") as file:
        file.write(column_content)
    print("Successfully updated column.html card grid with photo thumbnails and sidebar counts.")

    # Rebuild sitemap.xml with Clean URLs (no .html)
    print("Rebuilding sitemap.xml with clean URLs...")
    today_date = datetime.date.today().strftime('%Y-%m-%d')

    sitemap_entries = [
        ("https://re-en.jp/", "1.0", "daily"),
        ("https://re-en.jp/column", "0.9", "daily"),
        ("https://re-en.jp/preregister", "0.9", "weekly"),
        ("https://re-en.jp/pricing", "0.8", "monthly"),
        ("https://re-en.jp/privacy", "0.5", "monthly"),
        ("https://re-en.jp/term", "0.5", "monthly"),
        ("https://re-en.jp/tokushoho", "0.5", "monthly"),
        ("https://re-en.jp/company", "0.5", "monthly")
    ]

    for meta in detail_meta_list:
        file_loc = f"https://re-en.jp/{meta['clean_url']}"
        sitemap_entries.append((file_loc, "0.7", "monthly"))

    url_nodes = []
    for loc, priority, changefreq in sitemap_entries:
        url_nodes.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today_date}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(url_nodes)}
</urlset>"""

    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    print("Successfully updated sitemap.xml with clean URLs.")

if __name__ == "__main__":
    main()
