import os
import re
import glob

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

def add_toc_to_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Avoid duplicating TOC if already added
    if 'class="article-toc"' in content:
        return False

    # Extract H2 and H3 elements within article-body
    body_match = re.search(r'(?s)<div class="article-body">(.*?)<!-- Related Articles -->', content)
    if not body_match:
        return False

    body_content = body_match.group(1)

    # Parse headings and assign IDs
    toc_items = []
    sec_h2_idx = 0
    sec_h3_idx = 0

    def replace_h2(m):
        nonlocal sec_h2_idx, sec_h3_idx
        sec_h2_idx += 1
        sec_h3_idx = 0
        title = m.group(1)
        anchor_id = f"heading-{sec_h2_idx}"
        toc_items.append({"level": 2, "id": anchor_id, "title": title, "num": f"{sec_h2_idx}."})
        return f'<h2 id="{anchor_id}">{title}</h2>'

    def replace_h3(m):
        nonlocal sec_h2_idx, sec_h3_idx
        sec_h3_idx += 1
        title = m.group(1)
        anchor_id = f"heading-{sec_h2_idx}-{sec_h3_idx}"
        toc_items.append({"level": 3, "id": anchor_id, "title": title, "num": f"{sec_h2_idx}-{sec_h3_idx}."})
        return f'<h3 id="{anchor_id}">{title}</h3>'

    # Replace headings in body_content
    new_body_content = re.sub(r'<h2>(.*?)</h2>', replace_h2, body_content)
    new_body_content = re.sub(r'<h3>(.*?)</h3>', replace_h3, new_body_content)

    # Build TOC HTML
    toc_list_html = ""
    current_in_h3 = False

    for item in toc_items:
        if item["level"] == 2:
            if current_in_h3:
                toc_list_html += "</ul>\n</li>\n"
                current_in_h3 = False
            toc_list_html += f'<li class="article-toc__item article-toc__item--h2"><a href="#{item["id"]}">{item["title"]}</a>\n'
        elif item["level"] == 3:
            if not current_in_h3:
                toc_list_html += '<ul class="article-toc__sublist">\n'
                current_in_h3 = True
            toc_list_html += f'<li class="article-toc__item article-toc__item--h3"><a href="#{item["id"]}">{item["title"]}</a></li>\n'

    if current_in_h3:
        toc_list_html += "</ul>\n</li>\n"

    toc_html = f"""
              <!-- Article Table of Contents (TOC) -->
              <div class="article-toc">
                <div class="article-toc__header">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
                  <span>目次</span>
                </div>
                <ol class="article-toc__list">
                  {toc_list_html.strip()}
                </ol>
              </div>
"""

    # Insert TOC right after lead paragraph (<p class="article-lead">...</p>)
    if '<p class="article-lead"' in new_body_content:
        new_body_content = re.sub(
            r'(?s)(<p class="article-lead".*?</p>)',
            rf'\g<1>\n{toc_html}',
            new_body_content,
            count=1
        )
    else:
        # Fallback: insert at top of new_body_content
        new_body_content = toc_html + new_body_content

    # Reconstruct full HTML
    content = re.sub(r'(?s)(<div class="article-body">).*?(?=\s*<!-- Related Articles -->)', rf'\g<1>\n{new_body_content}', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True

def main():
    print("Injecting Table of Contents (TOC) into all column-detail files...")
    files = glob.glob(os.path.join(WORKSPACE_DIR, "column-detail*.html"))
    count = 0
    for f in files:
        if add_toc_to_html_file(f):
            count += 1
    print(f"Successfully added TOC to {count} column detail HTML files!")

if __name__ == "__main__":
    main()
