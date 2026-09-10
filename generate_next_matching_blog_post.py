import os
import re
import json
import datetime

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
CALENDAR_PATH = os.path.join(WORKSPACE_DIR, "editorial_calendar_matching.json")
TEMPLATE_PATH = os.path.join(WORKSPACE_DIR, "column-detail-52.html")

def get_num(name):
    if name == "column-detail.html":
        return 1
    num_part = re.sub(r'\D', '', name)
    return int(num_part) if num_part else 0

def get_vol_from_post(post):
    match = re.search(r'column-detail-(\d+)\.html', post["filename"])
    return int(match.group(1)) if match else 53

def main():
    print("Running generate_next_matching_blog_post.py (Image Thumbnail Mode)...")

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

    clean_url_name = target_post["filename"].replace('.html', '')
    canonical_url = f"https://re-en.jp/{clean_url_name}"

    # Truncated title for breadcrumbs (20 chars max + '...')
    breadcrumb_title = target_post["headline"]
    if len(breadcrumb_title) > 20:
        breadcrumb_title = breadcrumb_title[:20] + "..."

    # Use Photo Stock Image for Banner with safety fallback
    banner_img = target_post.get("banner_img", "images/column_second_partner.webp")
    if not os.path.exists(os.path.join(WORKSPACE_DIR, banner_img)):
        banner_img = "images/column_second_partner.webp"

    # 1. Update <title>
    new_html = re.sub(r'<title>.*?</title>', f'<title>{target_post["title"]}</title>', new_html)

    # 2. Update meta tags
    new_html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{target_post["description"]}">', new_html)
    new_html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{target_post["title"]}">', new_html)
    new_html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{target_post["description"]}">', new_html)
    new_html = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{canonical_url}">', new_html)
    new_html = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{canonical_url}">', new_html)

    # 3. Update JSON-LD BlogPosting
    blogposting_pattern = r'(?s)<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "BlogPosting".*?</script>'
    new_blogposting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": target_post["headline"],
        "image": [
            f"https://re-en.jp/{banner_img}"
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
            "name": "Re.en（リエン）",
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
                "item": "https://re-en.jp/column"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": breadcrumb_title,
                "item": canonical_url
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
            <li class="breadcrumbs__item"><a href="column">コラム一覧</a></li>
            <li class="breadcrumbs__separator">/</li>
            <li class="breadcrumbs__item" aria-current="page" style="color: var(--color-primary);">{breadcrumb_title}</li>
          </ul>"""
    new_html = re.sub(breadcrumbs_block_pattern, breadcrumbs_block_html, new_html)

    # 6. Update Visible Header details
    new_html = re.sub(r'<span class="article-header__category">[^<]+</span>', f'<span class="article-header__category">{target_post["category_name"]}</span>', new_html)
    new_html = re.sub(r'<span class="article-header__date">[^<]+</span>', f'<span class="article-header__date">{period_date}</span>', new_html)
    new_html = re.sub(r'<h1 class="article-header__title">[^<]+</h1>', f'<h1 class="article-header__title">{target_post["headline"]}</h1>', new_html)

    # 7. Update Hero visual Image (Photographic Thumbnail)
    hero_thumb_pattern = r'(?s)<div class="rec-article__thumb"[^>]*>.*?</div>'
    hero_thumb_html = f"""<div class="rec-article__thumb" style="width: 100%; height: 350px; overflow: hidden; border-radius: 4px; margin-bottom: 32px;"><img src="{banner_img}" alt="{target_post['headline']}" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.85; margin: 0; border: none;" loading="lazy" width="800" height="350"></div>"""
    new_html = re.sub(hero_thumb_pattern, hero_thumb_html, new_html)

    # Save the generated details file
    output_path = os.path.join(WORKSPACE_DIR, target_post["filename"])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"Successfully generated next blog post with photo thumbnail: {target_post['filename']}")

if __name__ == "__main__":
    main()
