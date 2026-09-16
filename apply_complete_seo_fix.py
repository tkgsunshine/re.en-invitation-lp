import os
import re
import glob
import json

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

def fix_page_meta_and_schema(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract vol number if column detail page
    vol_match = re.search(r'column-detail-(\d+)\.html', filename)
    vol_num = int(vol_match.group(1)) if vol_match else None

    # Canonical & Clean URL (no .html extension for cleanUrls compatibility)
    clean_name = filename.replace('.html', '') if filename != 'index.html' else ''
    canonical_url = f"https://re-en.jp/{clean_name}"

    # Check title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else "Re.en（リエン）| 完全審査制・既婚者限定サードプレイス"

    # Check description
    desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
    description = desc_match.group(1) if desc_match else "既婚者のための完全審査制上質コミュニティRe.en（リエン）。"

    # Determine og:image
    if vol_num:
        og_image = f"https://re-en.jp/images/column_{vol_num}.webp"
    else:
        og_image = "https://re-en.jp/images/hero_lifestyle.webp"

    safe_title = title.replace('"', '')
    safe_desc = description.replace('"', '')

    # Update or inject canonical link tag
    canonical_tag = f'<link rel="canonical" href="{canonical_url}">'
    if '<link rel="canonical"' in content:
        content = re.sub(r'<link rel="canonical" href="[^"]*">', canonical_tag, content)
    else:
        content = re.sub(r'(</title>)', r'\1\n  ' + canonical_tag, content, count=1)

    # Preconnect hints and Google Fonts optimization
    fonts_block = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Noto+Serif+JP:wght@500;700&family=Oswald:wght@500;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Noto+Serif+JP:wght@500;700&family=Oswald:wght@500;700&display=swap" rel="stylesheet"></noscript>"""

    # Replace old fonts links if present
    content = re.sub(
        r'(?:<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?\n)?(?:<link rel="preconnect" href="https://fonts\.gstatic\.com"[^>]*>.*?\n)?<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"[^>]*>(?:\s*<noscript><link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"></noscript>)?',
        fonts_block,
        content,
        flags=re.DOTALL
    )

    # OGP block
    ogp_html = f"""
  <!-- OGP & Social Meta Tags -->
  <meta property="og:title" content="{safe_title}">
  <meta property="og:description" content="{safe_desc}">
  <meta property="og:type" content="{'article' if vol_num else 'website'}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:site_name" content="Re.en（リエン）">
  <meta property="og:locale" content="ja_JP">
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
    "url": "{canonical_url}",
    "datePublished": "2026-09-01T09:00:00+09:00",
    "dateModified": "2026-09-09T09:00:00+09:00",
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
      "@id": "{canonical_url}"
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
        "item": "https://re-en.jp/column"
      }},
      {{
        "@type": "ListItem",
        "position": 3,
        "name": "{safe_title}",
        "item": "{canonical_url}"
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
