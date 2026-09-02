import os
import re
import glob
import json

WORKSPACE_DIR = "/Users/user/.gemini/antigravity/scratch/married-matching-lp"

def fix_page_meta_and_schema(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract vol number if column detail page
    vol_match = re.search(r'column-detail-(\d+)\.html', filename)
    vol_num = int(vol_match.group(1)) if vol_match else None

    # Check title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else "Re.en（リエン）| 完全審査制・既婚者限定マッチング"

    # Check description
    desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
    description = desc_match.group(1) if desc_match else "既婚者のための完全審査制上質コミュニティRe.en（リエン）。"

    # Page URL
    page_url = f"https://re-en.jp/{filename if filename != 'index.html' else ''}"

    # Determine og:image
    if vol_num:
        og_image = f"https://re-en.jp/images/column_{vol_num}.webp"
    else:
        og_image = "https://re-en.jp/images/hero_lifestyle.webp"

    safe_title = title.replace('"', '')
    safe_desc = description.replace('"', '')

    # OGP block
    ogp_html = f"""
  <!-- OGP & Social Meta Tags -->
  <meta property="og:title" content="{safe_title}">
  <meta property="og:description" content="{safe_desc}">
  <meta property="og:type" content="{'article' if vol_num else 'website'}">
  <meta property="og:url" content="{page_url}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:site_name" content="Re.en（リエン）">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{safe_title}">
  <meta name="twitter:description" content="{safe_desc}">
  <meta name="twitter:image" content="{og_image}">"""

    # Inject OGP if missing
    if 'property="og:image"' not in content and "property='og:image'" not in content:
        content = re.sub(r'(</title>)', r'\1' + ogp_html, content, count=1)

    # Inject BlogPosting + BreadcrumbList JSON-LD Schema if column detail page
    if vol_num:
        schema_jsonld = f"""
  <!-- Structured Data (JSON-LD) for Article & Breadcrumb -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{safe_title}",
    "description": "{safe_desc}",
    "image": "{og_image}",
    "url": "{page_url}",
    "datePublished": "2026-09-01",
    "dateModified": "2026-09-02",
    "author": {{
      "@type": "Organization",
      "name": "Re.en 編集部",
      "url": "https://re-en.jp/"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Re.en（リエン）",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://re-en.jp/images/favicon_centered.png"
      }}
    }},
    "mainEntityOfPage": {{
      "@type": "WebPage",
      "@id": "{page_url}"
    }}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{
        "@type": "ListItem",
        "position": 1,
        "name": "ホーム",
        "item": "https://re-en.jp/"
      }},
      {{
        "@type": "ListItem",
        "position": 2,
        "name": "コラム一覧",
        "item": "https://re-en.jp/column.html"
      }},
      {{
        "@type": "ListItem",
        "position": 3,
        "name": "{safe_title}",
        "item": "{page_url}"
      }}
    ]
  }}
  </script>"""

        if 'schema.org' not in content:
            content = re.sub(r'(</head>)', schema_jsonld + r'\n\1', content, count=1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True

def main():
    print("Running complete SEO audit fix across all HTML files...")
    files = glob.glob(os.path.join(WORKSPACE_DIR, "*.html"))
    for f in files:
        fix_page_meta_and_schema(f)
    print("Successfully injected missing OGP, Twitter cards, and JSON-LD schemas!")

if __name__ == "__main__":
    main()
