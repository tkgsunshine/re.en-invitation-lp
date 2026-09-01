import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.dirname(SCRIPT_DIR)

def main():
    print("Starting Married Matching LP Column Automation Pipeline...")
    
    # 1. Run generate_next_matching_blog_post.py
    print("\n--- Running: generate_next_matching_blog_post.py ---")
    subprocess.run(["python3", os.path.join(SCRIPT_DIR, "generate_next_matching_blog_post.py")], check=True)
    
    # 2. Run write_matching_article_contents.py
    print("\n--- Running: write_matching_article_contents.py ---")
    subprocess.run(["python3", os.path.join(SCRIPT_DIR, "write_matching_article_contents.py")], check=True)
    
    # 3. Run rebuild_matching_blog_index.py
    print("\n--- Running: rebuild_matching_blog_index.py ---")
    subprocess.run(["python3", os.path.join(SCRIPT_DIR, "rebuild_matching_blog_index.py")], check=True)
    
    # 4. Run apply_matching_seo_optimizations.py
    print("\n--- Running: apply_matching_seo_optimizations.py ---")
    subprocess.run(["python3", os.path.join(SCRIPT_DIR, "apply_matching_seo_optimizations.py")], check=True)
    
    # 5. Git Commit & Push to GitHub
    print("\\n--- Committing & Pushing to GitHub ---")
    subprocess.run(["git", "add", "-A"], cwd=WORKSPACE_DIR)
    subprocess.run(["git", "commit", "-m", "Auto-update columns and indexes via pipeline"], cwd=WORKSPACE_DIR)
    subprocess.run(["git", "push", "origin", "main"], cwd=WORKSPACE_DIR)

    # 6. Deploy to Vercel production
    print("\\n--- Deploying to Vercel Production ---")
    my_env = os.environ.copy()
    my_env["HOME"] = "/Users/user"
    subprocess.run(["npx", "vercel", "deploy", "--prod"], cwd=WORKSPACE_DIR, env=my_env, check=True)
    
    print("\\nMarried Matching LP Column Pipeline complete!")

if __name__ == "__main__":
    main()
