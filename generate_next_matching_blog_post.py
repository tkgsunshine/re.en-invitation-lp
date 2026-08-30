import os
import re
import json
import datetime

WORKSPACE_DIR = "/Users/user/.gemini/antigravity/scratch/married-matching-lp"
CALENDAR_PATH = os.path.join(WORKSPACE_DIR, "editorial_calendar_matching.json")
TEMPLATE_PATH = os.path.join(WORKSPACE_DIR, "column-detail-52.html")

def get_num(name):
    if name == "column-detail.html":
        return 1
    num_part = re.sub(r'\D', '', name)
    return int(num_part) if num_part else 0

def estimate_text_width(text, font_size):
    width = 0
    for char in text:
        if ord(char) < 128:
            width += font_size * 0.55
        else:
            width += font_size * 1.0
    return width

def get_vol_from_post(post):
    match = re.search(r'column-detail-(\d+)\.html', post["filename"])
    return int(match.group(1)) if match else 53

def main():
    print("Running generate_next_matching_blog_post.py...")

    if not os.path.exists(CALENDAR_PATH):
        print(f"Error: Calendar database not found at {CALENDAR_PATH}")
        return

    with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
        calendar = json.load(f)

    # 1. Detect the next ungenerated post volume
    existing_files = [f for f in os.listdir(WORKSPACE_DIR) if f.startswith("column-detail-") and f.endswith(".html")]
    existing_vols = {get_num(f) for f in existing_files}

    target_post = None
    for post in calendar:
        post_vol = get_vol_from_post(post)
        if post_vol not in existing_vols:
            target_post = post
            break

    if not target_post:
        print("No new columns to generate! All scheduled volumes already exist.")
        return

    target_vol = get_vol_from_post(target_post)
    print(f"Found next planned column: Vol.{target_vol} ({target_post['headline']})")

    # Read template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        new_html = f.read()

    # Dates
    today = datetime.date.today()
    period_date = today.strftime('%Y.%m.%d')
    iso_date = today.strftime('%Y-%m-%d')

    # Truncated title for breadcrumbs (20 chars max + '...')
    breadcrumb_title = target_post["headline"]
    if len(breadcrumb_title) > 20:
        breadcrumb_title = breadcrumb_title[:20] + "..."

    # Generate custom visual SVG banner (Premium Luxury Dark Gold Style)
    title_line1 = target_post["title_line1"]
    title_line2 = target_post["title_line2"]
    
    # Calculate font sizes for SVG titles
    font_size1 = 40
    width1 = estimate_text_width(title_line1, 40)
    if width1 > 750:
        font_size1 = int(40 * (750 / width1))
        if font_size1 < 26:
            font_size1 = 26

    font_size2 = 46
    width2 = estimate_text_width(title_line2, 46)
    if width2 > 750:
        font_size2 = int(46 * (750 / width2))
        if font_size2 < 28:
            font_size2 = 28

    svg_visual = f"""<svg viewBox="0 0 1000 428" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="「{target_post['headline']}」のプレミアムバナー" width="100%" height="100%" style="width: 100%; height: 100%; object-fit: cover; border: none; display: block;">
          <defs>
            <linearGradient id="gold-bg-grad" x1="0" y1="0" x2="1000" y2="428" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stop-color="#0e0e12" />
              <stop offset="50%" stop-color="#15151c" />
              <stop offset="100%" stop-color="#09090b" />
            </linearGradient>
            <linearGradient id="gold-accent-grad" x1="0" y1="0" x2="1000" y2="0" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stop-color="#F3E5AB" />
              <stop offset="50%" stop-color="#D4AF37" />
              <stop offset="100%" stop-color="#AA771C" />
            </linearGradient>
          </defs>
          <rect width="1000" height="428" fill="url(#gold-bg-grad)"/>
          
          <!-- Background geometric accents -->
          <path d="M 0 0 L 1000 428 M 1000 0 L 0 428" stroke="url(#gold-accent-grad)" stroke-width="0.5" opacity="0.05"/>
          <circle cx="500" cy="214" r="180" stroke="url(#gold-accent-grad)" stroke-width="1" opacity="0.06"/>
          
          <!-- Vol label in background -->
          <text x="500" y="260" text-anchor="middle" fill="#D4AF37" font-size="160" font-family="'Oswald', sans-serif" font-weight="700" opacity="0.02" letter-spacing="0.05em">VOL.{target_vol}</text>
          
          <!-- Double gold borders -->
          <rect x="20" y="20" width="960" height="388" rx="8" stroke="url(#gold-accent-grad)" stroke-width="1.5" opacity="0.25"/>
          <rect x="25" y="25" width="950" height="378" rx="6" stroke="url(#gold-accent-grad)" stroke-width="0.5" opacity="0.15"/>
          
          <!-- Category Label -->
          <text x="500" y="95" text-anchor="middle" fill="#D4AF37" font-size="13" font-family="'Noto Sans JP', sans-serif" font-weight="700" letter-spacing="0.4em">{target_post['category_name'].upper()}</text>
          <line x1="450" y1="110" x2="550" y2="110" stroke="url(#gold-accent-grad)" stroke-width="1" opacity="0.4"/>
          
          <!-- Main Japanese Titles -->
          <text x="500" y="195" text-anchor="middle" fill="url(#gold-accent-grad)" font-size="{font_size1}" font-family="'Noto Serif JP', serif" font-weight="700" letter-spacing="0.05em">{title_line1}</text>
          <text x="500" y="258" text-anchor="middle" fill="url(#gold-accent-grad)" font-size="{font_size2}" font-family="'Noto Serif JP', serif" font-weight="700" letter-spacing="0.05em">{title_line2}</text>
          
          <!-- English Tagline -->
          <text x="500" y="335" text-anchor="middle" fill="#8E8E9F" font-size="13" font-family="'Oswald', sans-serif" font-weight="400" letter-spacing="0.25em">{target_post['english_title']}</text>
        </svg>"""

    # 1. Update <title>
    new_html = re.sub(r'<title>.*?</title>', f'<title>{target_post["title"]}</title>', new_html)

    # 2. Update meta tags
    new_html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{target_post["description"]}">', new_html)
    new_html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{target_post["title"]}">', new_html)
    new_html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{target_post["description"]}">', new_html)
    new_html = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="https://re-en.jp/{target_post["filename"]}">', new_html)
    new_html = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://re-en.jp/{target_post["filename"]}">', new_html)

    # 3. Update JSON-LD BlogPosting
    blogposting_pattern = r'(?s)<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "BlogPosting".*?</script>'
    new_blogposting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": target_post["headline"],
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
        "description": target_post["description"]
    }
    blogposting_html = f'<script type="application/ld+json">\n  {json.dumps(new_blogposting, ensure_ascii=False, indent=2)}\n  </script>'
    new_html = re.sub(blogposting_pattern, blogposting_html, new_html)

    # 4. Update JSON-LD BreadcrumbList
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

    # 5. Update Visible Breadcrumbs
    breadcrumbs_block_pattern = r'(?s)<ul class="breadcrumbs">.*?</ul>'
    breadcrumbs_block_html = f"""<ul class="breadcrumbs">
            <li class="breadcrumbs__item"><a href="index.html">ホーム</a></li>
            <li class="breadcrumbs__separator">/</li>
            <li class="breadcrumbs__item"><a href="column.html">コラム一覧</a></li>
            <li class="breadcrumbs__separator">/</li>
            <li class="breadcrumbs__item" aria-current="page" style="color: var(--color-primary);">{breadcrumb_title}</li>
          </ul>"""
    new_html = re.sub(breadcrumbs_block_pattern, breadcrumbs_block_html, new_html)

    # 6. Update Visible Header details
    new_html = re.sub(r'<span class="article-header__category">[^<]+</span>', f'<span class="article-header__category">{target_post["category_name"]}</span>', new_html)
    new_html = re.sub(r'<span class="article-header__date">[^<]+</span>', f'<span class="article-header__date">{period_date}</span>', new_html)
    new_html = re.sub(r'<h1 class="article-header__title">[^<]+</h1>', f'<h1 class="article-header__title">{target_post["headline"]}</h1>', new_html)

    # 7. Update Hero visual SVG
    hero_thumb_pattern = r'(?s)<div class="rec-article__thumb"[^>]*>.*?</div>'
    hero_thumb_html = f"""<div class="rec-article__thumb" style="width: 100%; height: auto; overflow: hidden; border-radius: 8px; margin-bottom: 32px;">{svg_visual}</div>"""
    new_html = re.sub(hero_thumb_pattern, hero_thumb_html, new_html)

    # Save the generated details file
    output_path = os.path.join(WORKSPACE_DIR, target_post["filename"])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"Successfully generated next blog post raw file: {target_post['filename']}")

if __name__ == "__main__":
    main()
