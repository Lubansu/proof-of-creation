#!/usr/bin/env python3
"""
publish_to_github.py — Publishes proof-of-creation to GitHub automatically.

Usage (run in Claude Code or locally):
  python3 publish_to_github.py --token YOUR_GITHUB_TOKEN --username YOUR_USERNAME

What this script does:
  1. Creates the GitHub repository via API
  2. Initializes git locally
  3. Adds all files with proper commit message
  4. Pushes to GitHub
  5. Sets repository topics and description
  6. Creates v1.0.0 release
  7. Prints the PR template to submit to watermarks-remover ecosystem

Requirements:
  - Python 3.10+
  - git installed
  - A GitHub personal access token with 'repo' scope
    Create at: https://github.com/settings/tokens/new
    Required scopes: repo (full control of private repositories)
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

REPO_NAME = "proof-of-creation"
REPO_DESCRIPTION = "🛡️ Automatic AI copyright protection — proves ownership of code you create with any LLM. Headers, SHA-256 hashes, legal guidance for 15+ countries."
REPO_TOPICS = [
    "claude-code", "claude", "anthropic", "ip-protection",
    "copyright", "legal", "skill", "watermark",
    "intellectual-property", "license", "open-source"
]
AUTHOR_NAME = "Lubansu Alphonse"
AUTHOR_EMAIL = "alubansu@gmail.com"  # Override with --email if needed


def github_api(path: str, method: str = "GET", data: dict = None, token: str = "") -> dict:
    """Make a GitHub API request."""
    url = f"https://api.github.com{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = json.loads(e.read())
        detail = error_body.get("message", e.reason)
        field_errors = error_body.get("errors")
        if field_errors:
            detail += " | " + "; ".join(
                f"{fe.get('field', '?')}: {fe.get('message') or fe.get('code', '?')}"
                for fe in field_errors
            )
        raise RuntimeError(f"GitHub API error {e.code}: {detail}")


def run(cmd: list, cwd: str = None, env: dict = None) -> str:
    """Run a shell command and return output."""
    run_env = dict(env) if env is not None else dict(os.environ)
    # Force English git output so substring checks (e.g. "nothing to commit")
    # work regardless of the user's terminal locale.
    run_env["LC_ALL"] = "C"
    run_env["LANG"] = "C"
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=run_env)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
    return result.stdout.strip()


def main():
    parser = argparse.ArgumentParser(description="Publish proof-of-creation to GitHub")
    parser.add_argument("--token", required=True, help="GitHub personal access token (repo scope)")
    parser.add_argument("--username", required=True, help="Your GitHub username")
    parser.add_argument("--email", default=AUTHOR_EMAIL, help="Your email for git config")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without doing it")
    args = parser.parse_args()

    repo_dir = Path(__file__).parent
    remote_url = f"https://{args.token}@github.com/{args.username}/{REPO_NAME}.git"

    print(f"\n🛡️  proof-of-creation → GitHub Publisher")
    print(f"   Author : {AUTHOR_NAME} ({args.username})")
    print(f"   Repo   : github.com/{args.username}/{REPO_NAME}")
    print(f"   Dry run: {args.dry_run}\n")

    # --- Step 1: Create GitHub repository ---
    print("→ Step 1: Creating GitHub repository...")
    if not args.dry_run:
        try:
            repo = github_api("/user/repos", method="POST", token=args.token, data={
                "name": REPO_NAME,
                "description": REPO_DESCRIPTION,
                "private": False,
                "auto_init": False,
                "has_issues": True,
                "has_discussions": True,
            })
            print(f"  ✅ Repository created: {repo['html_url']}")
        except RuntimeError as e:
            if "already exists" in str(e):
                print(f"  ℹ️  Repository already exists — continuing with push")
            else:
                raise
    else:
        print(f"  [dry-run] Would create: github.com/{args.username}/{REPO_NAME}")

    # --- Step 2: Initialize git ---
    print("\n→ Step 2: Initializing git...")
    env = {**os.environ, "GIT_AUTHOR_NAME": AUTHOR_NAME, "GIT_COMMITTER_NAME": AUTHOR_NAME,
           "GIT_AUTHOR_EMAIL": args.email, "GIT_COMMITTER_EMAIL": args.email}

    if not args.dry_run:
        if not (repo_dir / ".git").exists():
            run(["git", "init", "-b", "main"], cwd=str(repo_dir))
            run(["git", "config", "user.name", AUTHOR_NAME], cwd=str(repo_dir))
            run(["git", "config", "user.email", args.email], cwd=str(repo_dir))
            print("  ✅ Git initialized")
        else:
            print("  ℹ️  Git already initialized")
    else:
        print("  [dry-run] Would initialize git")

    # --- Step 3: Add and commit files ---
    print("\n→ Step 3: Committing files...")
    if not args.dry_run:
        run(["git", "add", "."], cwd=str(repo_dir), env=env)
        try:
            run(["git", "commit", "-m",
                 "feat: initial release v1.0.0\n\n"
                 "- proof-of-creation skill for Claude Code\n"
                 "- Automatic copyright header injection on file creation\n"
                 "- SHA-256 proof-of-creation hashing\n"
                 "- Legal guidance for 15+ jurisdictions (FR, EU, US, UK, CA...)\n"
                 "- Combined workflow with watermarks-remover\n"
                 "- Bilingual README (FR/EN)\n"
                 "- MIT license\n\n"
                 f"Author: {AUTHOR_NAME}"],
                cwd=str(repo_dir), env=env)
            print("  ✅ Initial commit created")
        except RuntimeError as e:
            if "nothing to commit" in str(e):
                print("  ℹ️  Nothing new to commit")
            else:
                raise
    else:
        print("  [dry-run] Would commit all files")

    # --- Step 4: Push to GitHub ---
    print("\n→ Step 4: Pushing to GitHub...")
    if not args.dry_run:
        try:
            run(["git", "remote", "add", "origin", remote_url], cwd=str(repo_dir))
        except RuntimeError:
            run(["git", "remote", "set-url", "origin", remote_url], cwd=str(repo_dir))
        run(["git", "push", "-u", "origin", "main"], cwd=str(repo_dir), env=env)
        print(f"  ✅ Pushed to github.com/{args.username}/{REPO_NAME}")
    else:
        print("  [dry-run] Would push to GitHub")

    # --- Step 5: Set topics ---
    print("\n→ Step 5: Setting repository topics...")
    if not args.dry_run:
        github_api(f"/repos/{args.username}/{REPO_NAME}/topics",
                   method="PUT", token=args.token, data={"names": REPO_TOPICS})
        print(f"  ✅ Topics set: {', '.join(REPO_TOPICS)}")
    else:
        print(f"  [dry-run] Would set topics: {', '.join(REPO_TOPICS)}")

    # --- Step 6: Create release ---
    print("\n→ Step 6: Creating v1.0.0 release...")
    if not args.dry_run:
        run(["git", "tag", "-a", "v1.0.0", "-m", "Initial release v1.0.0"], cwd=str(repo_dir), env=env)
        run(["git", "push", "origin", "v1.0.0"], cwd=str(repo_dir), env=env)
        github_api(f"/repos/{args.username}/{REPO_NAME}/releases",
                   method="POST", token=args.token, data={
                       "tag_name": "v1.0.0",
                       "name": "v1.0.0 — Initial Release",
                       "body": (
                           "## proof-of-creation v1.0.0\n\n"
                           "First public release of the Proof of Creation skill for Claude Code.\n\n"
                           "### Features\n"
                           "- Automatic copyright header injection on every file Claude creates\n"
                           "- SHA-256 proof-of-creation hashing with timestamped log\n"
                           "- Context-aware license recommendations\n"
                           "- Legal guidance for 15+ jurisdictions (France, EU, USA, UK, Canada...)\n"
                           "- Combined workflow with watermarks-remover\n"
                           "- Commands: /proof-of-creation, /ip-report, /ip-hash, /ip-license, /ip-register, /ip-workflow\n\n"
                           "### Install\n"
                           "```\n"
                           f"/plugin marketplace add {args.username}/proof-of-creation\n"
                           "/plugin install proof-of-creation@proof-of-creation\n"
                           "```\n"
                       ),
                       "draft": False,
                       "prerelease": False,
                   })
        print("  ✅ Release v1.0.0 created")
    else:
        print("  [dry-run] Would create release v1.0.0")

    # --- Step 7: PR template for watermarks-remover ecosystem ---
    print("\n→ Step 7: PR template for watermarks-remover ecosystem")
    pr_body = f"""
## Add proof-of-creation to Ecosystem

### Project

**[proof-of-creation](https://github.com/{args.username}/{REPO_NAME})** by Lubansu Alphonse

### What it does

A Claude Code skill that automatically protects intellectual property in files
Claude creates: copyright header injection, SHA-256 proof-of-creation hashing,
and multi-jurisdiction legal guidance (15+ countries).

### How it integrates with watermarks-remover

The two skills form a complementary sequential workflow:

1. **proof-of-creation** runs first (automatic) — asserts creator ownership at creation time
2. **watermarks-remover** runs second (on demand) — strips AI provenance marks for distribution
3. `/ip-workflow` command guides users through both steps when both skills are installed

See [WORKFLOW.md](https://github.com/{args.username}/{REPO_NAME}/blob/main/WORKFLOW.md)
for full documentation of the combined workflow.

### Why it belongs in the Ecosystem section

Per your ecosystem policy: this project integrates with watermarks-remover
by referencing it in SKILL.md, WORKFLOW.md, and README.md, and the
`/ip-workflow` command detects whether watermarks-remover is installed and
adapts its guidance accordingly.

### Suggested entry

```markdown
### proof-of-creation — Proof of Creation for Claude Code

[proof-of-creation](https://github.com/{args.username}/{REPO_NAME}) is an MIT-licensed
Claude Code skill by Lubansu Alphonse. It automatically asserts creator ownership
on every file Claude writes (copyright headers, SHA-256 hashes, legal guidance for
15+ jurisdictions) and includes a combined `/ip-workflow` command that guides users
through both watermark removal and Proof of Creation sequentially.
```
"""

    print("\n" + "="*60)
    print("📋 COPY THIS TO OPEN A PR ON watermarks-remover:")
    print("   URL: https://github.com/guillaumemeyer/watermarks-remover/issues/new")
    print("="*60)
    print(pr_body)

    # --- Done ---
    print("\n" + "="*60)
    print("✅ All done!")
    print(f"   Your skill: https://github.com/{args.username}/{REPO_NAME}")
    print(f"   Install:    /plugin marketplace add {args.username}/{REPO_NAME}")
    print("="*60)


if __name__ == "__main__":
    main()
