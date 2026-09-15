import os
import re
import json

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
CALENDAR_PATH = os.path.join(WORKSPACE_DIR, "editorial_calendar_matching.json")

def clean_html(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = " ".join(text.split())
    return text.strip()

def get_vol_from_post(post):
    match = re.search(r'column-detail-(\d+)\.html', post["filename"])
    return int(match.group(1)) if match else 53

def main():
    print("Running write_matching_article_contents.py...")

    if not os.path.exists(CALENDAR_PATH):
        print(f"Error: Calendar database not found at {CALENDAR_PATH}")
        return

    with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
        calendar = json.load(f)

    # Scan and process all files that are missing the custom 'in-body-cta'
    updated_files = []
    for post in calendar:
        post_vol = get_vol_from_post(post)
        if post_vol == 52:
            continue
            
        path = os.path.join(WORKSPACE_DIR, post["filename"])
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            if "in-body-cta" not in content:
                print(f"Injecting copywriting into {post['filename']} (Vol.{post_vol})...")
                
                # Build the rich article body HTML
                body_html = ""
                for sec in post["body_sections"]:
                    body_html += f"\n              <h2>{sec['h2']}</h2>\n              {sec['text']}\n"

                # Add highlight box
                highlight_items = ""
                for item in post["highlight_box"]["items"]:
                    highlight_items += f"\n                <p>{item}</p>"

                body_html += f"""
              <div class="highlight-box">
                <div class="highlight-box__title">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                  {post['highlight_box']['title']}
                </div>{highlight_items}
              </div>"""

                # Add styled in-body CTA box promoting member registration (Aligning with Re.en aesthetic)
                body_html += """
              <div class="in-body-cta" style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--color-border-light); border-radius: 8px; padding: 28px 24px; margin: 40px 0; text-align: center;">
                <h3 style="font-size: 1.2rem; color: var(--color-primary); margin-bottom: 12px; font-weight: 700;">Re.en 創設メンバー事前インビテーション受付中</h3>
                <p style="font-size: 0.95rem; margin-bottom: 20px; color: var(--text-muted); line-height: 1.6;">Re.en（リエン）は、完全審査制の上質な既婚者限定コミュニティです。<br>現在、創設メンバー限定特典（有料プレミアムプラン2ヶ月間完全無料提供）の事前審査エントリーを受付中です。</p>
                <a href="https://re-en.jp/" class="btn btn--primary" style="display: inline-block; padding: 12px 32px; font-weight: 700; text-decoration: none;">優先インビテーションに申し込む</a>
            </div>"""

                # Estimate read time (roughly 500 characters per minute)
                char_count = len(clean_html(body_html))
                read_time = max(2, int(char_count / 500))

                # Replace read time
                content = re.sub(
                    r'<span class="article-header__readtime">読了目安: [^<]+</span>',
                    f'<span class="article-header__readtime">読了目安: {read_time}分</span>',
                    content
                )

                # Replace visible article body using safe landmark-based regex (matching B2B structure or Re.en structure)
                body_replacement_pattern = r'(?s)(<div class="article-body">).*?(?=\s*<!-- Related Articles -->)'
                content = re.sub(body_replacement_pattern, rf'\g<1>{body_html}\n            </div>', content)

                # Save file
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                updated_files.append(post["filename"])

    if updated_files:
        print(f"Successfully injected content and updated read times for: {', '.join(updated_files)}")
    else:
        print("No files required content injection.")

if __name__ == "__main__":
    main()
