import os
import subprocess

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print("Starting Married Matching LP Column Automation Pipeline...")
    
    # 1. Run generate_next_matching_blog_post.py
    print("\n--- Step 1: Generating next scheduled blog post template ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "generate_next_matching_blog_post.py")], check=True)
    
    # 2. Run write_matching_article_contents.py
    print("\n--- Step 2: Injecting base contents ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "write_matching_article_contents.py")], check=True)
    
    # 3. Run rewrite_all_columns_rich.py (Regulation: 2,500+ pure text characters)
    print("\n--- Step 3: Enriching content to 2,500+ pure text characters ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "rewrite_all_columns_rich.py")], check=True)

    # 4. Run fix_toc_tags.py (Regulation: Interactive Table of Contents)
    print("\n--- Step 4: Generating Table of Contents (TOC) & anchors ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "fix_toc_tags.py")], check=True)

    # 5. Run rebuild_matching_blog_index.py
    print("\n--- Step 5: Rebuilding column.html, sidebar, and sitemap.xml ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "rebuild_matching_blog_index.py")], check=True)
    
    # 6. Run apply_complete_seo_fix.py (Regulation: OGP, Twitter Cards, JSON-LD)
    print("\n--- Step 6: Applying complete SEO optimizations (OGP, Twitter Cards, JSON-LD) ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "apply_complete_seo_fix.py")], check=True)
    
    # 7. Git Commit & Push to GitHub
    print("\n--- Step 7: Committing & Pushing to GitHub ---")
    try:
        subprocess.run(["git", "add", "-A"], cwd=WORKSPACE_DIR, check=True)
        res = subprocess.run(["git", "status", "--porcelain"], cwd=WORKSPACE_DIR, capture_output=True, text=True)
        if res.stdout.strip():
            subprocess.run(["git", "commit", "-m", "Auto-publish daily column with full regulation compliance"], cwd=WORKSPACE_DIR, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=WORKSPACE_DIR, check=True)
        else:
            print("Working tree clean, nothing to commit.")
    except Exception as e:
        print(f"Git commit/push notice: {e}")

    # 8. Deploy to Vercel production
    print("\n--- Step 8: Deploying to Vercel Production ---")
    try:
        my_env = os.environ.copy()
        if "HOME" not in my_env or not my_env["HOME"]:
            my_env["HOME"] = "/tmp"
        subprocess.run(["npx", "vercel", "deploy", "--prod"], cwd=WORKSPACE_DIR, env=my_env, check=True)
    except Exception as e:
        print(f"Vercel CLI deployment notice (GitHub integration handles auto-deploy): {e}")
    
    print("\nMarried Matching LP Column Pipeline complete!")

if __name__ == "__main__":
    main()
