import os
import re
import datetime

WORKSPACE_DIR = "/Users/user/.gemini/antigravity/scratch/married-matching-lp"
SITEMAP_PATH = os.path.join(WORKSPACE_DIR, "sitemap.xml")

def get_num(name):
    if name == "column-detail.html":
        return 1
    num_part = re.sub(r'\D', '', name)
    return int(num_part) if num_part else 0

def main():
    print("Running rebuild_matching_blog_index.py...")

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
            readtime = readtime_match.group(1).strip() if readtime_match else "2分"
            
            # Detect SVG visual cover first, otherwise default to WebP image
            svg_match = re.search(r'(?s)<svg viewBox="0 0 1000 428"[^>]*>.*?</svg>', content)
            
            visual_html = ""
            img_path = "images/column_second_partner.webp"
            alt_text = ""
            
            if svg_match:
                # Add responsive styles to SVG
                svg_content = svg_match.group(0)
                # Inject width="100%" height="100%" and style if not present
                if 'width="100%"' not in svg_content:
                    svg_content = svg_content.replace('<svg viewBox=', '<svg width="100%" height="100%" style="width: 100%; height: 100%; object-fit: cover; border: none; display: block;" viewBox=')
                visual_html = svg_content
            else:
                img_match = re.search(r'(?s)<div class="rec-article__thumb"[^>]*>\s*<img src="([^"]+)" alt="([^"]+)"', content)
                if img_match:
                    img_path = img_match.group(1).strip()
                    alt_text = img_match.group(2).strip()
                    visual_html = f'<img src="{img_path}" alt="{alt_text}" class="column-card__img" loading="lazy">'
                else:
                    visual_html = f'<img src="{img_path}" alt="{alt_text}" class="column-card__img" loading="lazy">'
            
            if cat in cat_counts:
                cat_counts[cat] += 1
            
            detail_meta_list.append({
                "filename": f,
                "vol": get_num(f),
                "category": cat,
                "date": date,
                "title": title,
                "excerpt": excerpt,
                "visual_html": visual_html,
                "readtime": readtime
            })

    total_count = len(detail_meta_list)
    print(f"Total columns counted: {total_count}. Category breakdown: {cat_counts}")

    # Synchronize sidebar Categories Widget across all column details files
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

    # Rebuild the Card Grid in column.html
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
                  {meta['visual_html']}
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

    # Rebuild sitemap.xml
    print("Rebuilding sitemap.xml...")
    if os.path.exists(SITEMAP_PATH):
        import xml.etree.ElementTree as ET
        import xml.dom.minidom
        
        ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")
        tree = ET.parse(SITEMAP_PATH)
        root = tree.getroot()
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Collect loc URLs that currently exist in sitemap.xml
        existing_locs = set()
        for url_elem in root.findall('sm:url', ns):
            loc_elem = url_elem.find('sm:loc', ns)
            if loc_elem is not None:
                existing_locs.add(loc_elem.text)

        # For any column html file, check if it's in the sitemap. If not, add it
        today_date = datetime.date.today().strftime('%Y-%m-%d')
        updated = False
        
        for meta in detail_meta_list:
            file_loc = f"https://re-en.jp/{meta['filename']}"
            if file_loc not in existing_locs:
                url_elem = ET.Element('url')
                
                loc_elem = ET.SubElement(url_elem, 'loc')
                loc_elem.text = file_loc
                
                lastmod_elem = ET.SubElement(url_elem, 'lastmod')
                lastmod_elem.text = today_date
                
                changefreq_elem = ET.SubElement(url_elem, 'changefreq')
                changefreq_elem.text = "monthly"
                
                priority_elem = ET.SubElement(url_elem, 'priority')
                priority_elem.text = "0.7"
                
                root.append(url_elem)
                updated = True
                
        if updated:
            xml_str = ET.tostring(root, encoding='utf-8')
            parsed = xml.dom.minidom.parseString(xml_str)
            pretty_xml = parsed.toprettyxml(indent="  ")
            clean_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip()])
            
            if not clean_xml.startswith('<?xml'):
                clean_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + clean_xml
                
            with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
                f.write(clean_xml)
            print("Successfully updated sitemap.xml with missing column URLs.")
        else:
            print("Sitemap is already up-to-date.")

if __name__ == "__main__":
    main()
