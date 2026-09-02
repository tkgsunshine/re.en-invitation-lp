import os
import subprocess

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print("Starting Married Matching LP Column Automation Pipeline...")
    
    # 1. Run generate_next_matching_blog_post.py
    print("\n--- Running: generate_next_matching_blog_post.py ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "generate_next_matching_blog_post.py")], check=True)
    
    # 2. Run write_matching_article_contents.py
    print("\n--- Running: write_matching_article_contents.py ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "write_matching_article_contents.py")], check=True)
    
    # 3. Run rebuild_matching_blog_index.py
    print("\n--- Running: rebuild_matching_blog_index.py ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "rebuild_matching_blog_index.py")], check=True)
    
    # 4. Run apply_matching_seo_optimizations.py
    print("\n--- Running: apply_matching_seo_optimizations.py ---")
    subprocess.run(["python3", os.path.join(WORKSPACE_DIR, "apply_matching_seo_optimizations.py")], check=True)
    
    # 5. Git Commit & Push to GitHub
    print("\n--- Committing & Pushing to GitHub ---")
    try:
        subprocess.run(["git", "add", "-A"], cwd=WORKSPACE_DIR, check=True)
        res = subprocess.run(["git", "status", "--porcelain"], cwd=WORKSPACE_DIR, capture_output=True, text=True)
        if res.stdout.strip():
            subprocess.run(["git", "commit", "-m", "Auto-update columns and indexes via pipeline"], cwd=WORKSPACE_DIR, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=WORKSPACE_DIR, check=True)
        else:
            print("Working tree clean, nothing to commit.")
    except Exception as e:
        print(f"Git commit/push notice: {e}")

    # 6. Deploy to Vercel production
    print("\n--- Deploying to Vercel Production ---")
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
