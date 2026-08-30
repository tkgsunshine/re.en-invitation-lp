import os
import subprocess

WORKSPACE_DIR = "/Users/user/.gemini/antigravity/scratch/married-matching-lp"

def main():
    print("Starting Married Matching LP Column Automation Pipeline...")
    
    # 1. Run generate_next_matching_blog_post.py
    print("\\n--- Running: generate_next_matching_blog_post.py ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "generate_next_matching_blog_post.py")], check=True)
    
    # 2. Run write_matching_article_contents.py
    print("\\n--- Running: write_matching_article_contents.py ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "write_matching_article_contents.py")], check=True)
    
    # 3. Run rebuild_matching_blog_index.py
    print("\\n--- Running: rebuild_matching_blog_index.py ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "rebuild_matching_blog_index.py")], check=True)
    
    # 4. Run apply_matching_seo_optimizations.py
    print("\\n--- Running: apply_matching_seo_optimizations.py ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "apply_matching_seo_optimizations.py")], check=True)
    
    # 5. Deploy to Vercel production
    print("\\n--- Deploying to Vercel Production ---")
    subprocess.run(["npx", "vercel", "deploy", "--prod"], cwd=WORKSPACE_DIR, check=True)
    
    print("\\nMarried Matching LP Column Pipeline complete!")

if __name__ == "__main__":
    main()
