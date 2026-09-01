import os
import re
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.dirname(SCRIPT_DIR)
CALENDAR_PATH = os.path.join(SCRIPT_DIR, "editorial_calendar_matching.json")

def get_vol_from_post(post):
    match = re.search(r'column-detail-(\d+)\.html', post["filename"])
    return int(match.group(1)) if match else 53

def main():
    print("Running apply_matching_seo_optimizations.py...")

    if not os.path.exists(CALENDAR_PATH):
        print(f"Error: Calendar database not found at {CALENDAR_PATH}")
        return

    with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
        calendar = json.load(f)

    # Detect which file was just generated
    target_post = None
    for post in calendar:
        path = os.path.join(WORKSPACE_DIR, post["filename"])
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # If the file exists but doesn't have the FAQPage schema, we optimize it.
            if "FAQPage" not in content:
                post_vol = get_vol_from_post(post)
                if post_vol != 52:
                    target_post = post
                    break

    if not target_post:
        print("No unoptimized details pages detected to apply FAQ schema to.")
        return

    if "questions" not in target_post or not target_post["questions"]:
        print(f"No FAQ questions found in calendar for {target_post['filename']}. Skipping SEO optimizations.")
        return

    print(f"Injecting FAQPage JSON-LD schema into {target_post['filename']}...")

    # Build the FAQPage schema
    faq_entities = []
    for qa in target_post["questions"]:
        faq_entities.append({
            "@type": "Question",
            "name": qa["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": qa["a"]
            }
        })

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_entities
    }

    faq_schema_html = f"""  <script type="application/ld+json">
  {json.dumps(faq_schema, ensure_ascii=False, indent=2)}
  </script>
</head>"""

    # Read current file content
    filepath = os.path.join(WORKSPACE_DIR, target_post["filename"])
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Inject right before </head>
    content = re.sub(r'</head>', faq_schema_html, content)

    # Save file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully optimized SEO with FAQPage schema in {target_post['filename']}")

if __name__ == "__main__":
    main()
