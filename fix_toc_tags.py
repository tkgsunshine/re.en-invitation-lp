import os
import re
import glob

WORKSPACE_DIR = "/Users/user/.gemini/antigravity/scratch/married-matching-lp"

def fix_toc_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove existing TOC and heading IDs first
    content = re.sub(r'(?s)\s*<!-- Article Table of Contents \(TOC\) -->.*?</div>\s*', '\n', content)
    content = re.sub(r'<h([23]) id="heading-[^"]+">(.*?)</h\1>', r'<h\1>\2</h\1>', content)

    # Extract headings and build clean HTML structure
    body_match = re.search(r'(?s)<div class="article-body">(.*?)<!-- Related Articles -->', content)
    if not body_match:
        return False

    body_content = body_match.group(1)

    sec_h2_idx = 0
    sec_h3_idx = 0
    toc_structure = [] # list of dicts: {'h2': ..., 'h2_id': ..., 'sub': [{'h3': ..., 'h3_id': ...}]}

    def replace_h2(m):
        nonlocal sec_h2_idx, sec_h3_idx
        sec_h2_idx += 1
        sec_h3_idx = 0
        title = m.group(1)
        anchor_id = f"heading-{sec_h2_idx}"
        toc_structure.append({"h2": title, "h2_id": anchor_id, "sub": []})
        return f'<h2 id="{anchor_id}">{title}</h2>'

    def replace_h3(m):
        nonlocal sec_h2_idx, sec_h3_idx
        sec_h3_idx += 1
        title = m.group(1)
        anchor_id = f"heading-{sec_h2_idx}-{sec_h3_idx}"
        if toc_structure:
            toc_structure[-1]["sub"].append({"h3": title, "h3_id": anchor_id})
        return f'<h3 id="{anchor_id}">{title}</h3>'

    new_body_content = re.sub(r'<h2>(.*?)</h2>', replace_h2, body_content)
    new_body_content = re.sub(r'<h3>(.*?)</h3>', replace_h3, new_body_content)

    # Construct 100% valid HTML TOC
    toc_lis = []
    for h2_item in toc_structure:
        sub_lis = []
        for h3_item in h2_item["sub"]:
            sub_lis.append(f'<li class="article-toc__item article-toc__item--h3"><a href="#{h3_item["h3_id"]}">{h3_item["h3"]}</a></li>')
        
        if sub_lis:
            sub_html = f'<ul class="article-toc__sublist">\n' + "\n".join(sub_lis) + '\n</ul>'
            toc_lis.append(f'<li class="article-toc__item article-toc__item--h2"><a href="#{h2_item["h2_id"]}">{h2_item["h2"]}</a>\n{sub_html}\n</li>')
        else:
            toc_lis.append(f'<li class="article-toc__item article-toc__item--h2"><a href="#{h2_item["h2_id"]}">{h2_item["h2"]}</a></li>')

    toc_ol_inner = "\n".join(toc_lis)

    toc_html = f"""
              <!-- Article Table of Contents (TOC) -->
              <div class="article-toc">
                <div class="article-toc__header">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
                  <span>目次</span>
                </div>
                <ol class="article-toc__list">
{toc_ol_inner}
                </ol>
              </div>
"""

    if '<p class="article-lead"' in new_body_content:
        new_body_content = re.sub(
            r'(?s)(<p class="article-lead".*?</p>)',
            rf'\g<1>\n{toc_html}',
            new_body_content,
            count=1
        )
    else:
        new_body_content = toc_html + new_body_content

    content = re.sub(r'(?s)(<div class="article-body">).*?(?=\s*<!-- Related Articles -->)', rf'\g<1>\n{new_body_content}', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True

def main():
    print("Fixing TOC HTML tags across all column detail files...")
    files = glob.glob(os.path.join(WORKSPACE_DIR, "column-detail*.html"))
    for f in files:
        fix_toc_in_file(f)
    print("Successfully fixed TOC HTML structure for all column files!")

if __name__ == "__main__":
    main()
