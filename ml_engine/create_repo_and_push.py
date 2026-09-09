import sys
import os
import subprocess
import urllib.request
import json

def create_and_push(github_token, repo_name="SIH26003-Dementia-Cognitive-Platform"):
    username = "oshikatiwari"
    project_dir = "C:\\Users\\Oshika Tiwari\\.gemini\\antigravity\\scratch\\dementia_cognitive_platform"

    print(f"[*] Creating repository '{repo_name}' on GitHub for user '{username}'...")
    url = "https://api.github.com/user/repos"
    payload = json.dumps({
        "name": repo_name,
        "description": "SIH26003: AI-Based Cognitive Gaming and Memory Assistance Platform for Elderly Dementia Patients in NER",
        "private": False,
        "auto_init": False
    }).encode('utf-8')

    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "SIH26003-Uploader"
    })

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            repo_url = res_data.get("clone_url", f"https://github.com/{username}/{repo_name}.git")
            print(f"[+] Repository successfully created on GitHub: {repo_url}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        if e.code == 422: # Already exists
            print(f"[!] Repository '{repo_name}' already exists on GitHub.")
            repo_url = f"https://github.com/{username}/{repo_name}.git"
        else:
            print(f"[-] GitHub API Error ({e.code}): {error_body}")
            sys.exit(1)
    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)

    # Set authenticated git remote URL and push
    auth_remote_url = f"https://{username}:{github_token}@github.com/{username}/{repo_name}.git"
    
    print("[*] Setting git remote origin...")
    subprocess.run(["git", "remote", "remove", "origin"], cwd=project_dir, capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", auth_remote_url], cwd=project_dir, check=True)

    print("[*] Pushing all files, ML models, datasets, and Flutter app to GitHub...")
    push_res = subprocess.run(["git", "push", "-u", "origin", "main"], cwd=project_dir, capture_output=True, text=True)
    
    if push_res.returncode == 0:
        print(f"\n[✓] SUCCESS! All files pushed to: https://github.com/{username}/{repo_name}")
    else:
        print(f"[-] Push failed:\n{push_res.stderr}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
        create_and_push(token)
    else:
        print("Usage: python create_repo_and_push.py <GITHUB_PERSONAL_ACCESS_TOKEN>")
