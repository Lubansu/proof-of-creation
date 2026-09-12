#!/usr/bin/env python3
"""
install_skill.py — proof-of-creation skill installer
Installs the proof-of-creation skill for Claude Code, Cowork, or Cursor.

Usage:
  python3 install_skill.py --skill proof-of-creation --target claude-code
  python3 install_skill.py --skill proof-of-creation --target claude-project --project-dir /path/to/project
  python3 install_skill.py --skill proof-of-creation --target cowork
  python3 install_skill.py --list
"""

import argparse
import os
import shutil
import sys
import zipfile
from pathlib import Path
from datetime import datetime

SKILLS = {
    "proof-of-creation": {
        "description": "Automatic Proof of Creation — copyright headers, SHA-256 hashes, legal guidance",
        "path": "skills/proof-of-creation",
    }
}

TARGETS = {
    "claude-code": "~/.claude/skills",
    "cursor": "~/.cursor/skills",
    "cowork": "dist",
}


def validate_skill(skill_path: Path) -> list[str]:
    """Validate skill against Agent Skills packaging rules."""
    errors = []
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"Missing SKILL.md in {skill_path}")
        return errors

    content = skill_md.read_text(encoding="utf-8")
    if "name:" not in content:
        errors.append("SKILL.md missing 'name' field")
    if "description:" not in content:
        errors.append("SKILL.md missing 'description' field")
    if "license:" not in content:
        errors.append("SKILL.md missing 'license' field")

    return errors


def install_to_dir(skill_path: Path, target_dir: Path, skill_name: str, force: bool = False, link: bool = False):
    """Copy or symlink skill to target directory."""
    dest = target_dir / skill_name

    if dest.exists() and not force:
        # Backup existing
        backup = target_dir / f"{skill_name}.backup.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        shutil.move(str(dest), str(backup))
        print(f"  Existing install backed up to: {backup}")

    if link:
        if dest.exists():
            dest.unlink() if dest.is_symlink() else shutil.rmtree(dest)
        dest.symlink_to(skill_path.resolve())
        print(f"  Symlinked: {skill_path} → {dest}")
    else:
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(str(skill_path), str(dest))
        print(f"  Copied to: {dest}")


def package_cowork(skill_path: Path, skill_name: str, dist_dir: Path):
    """Package skill as ZIP for Cowork upload."""
    dist_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dist_dir / f"{skill_name}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in skill_path.rglob("*"):
            if file.is_file():
                arcname = skill_name / file.relative_to(skill_path)
                zf.write(file, arcname)

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    if size_mb > 30:
        print(f"  ⚠️  Bundle is {size_mb:.1f}MB — exceeds 30MB Cowork upload limit")
    else:
        print(f"  ✅ Bundle created: {zip_path} ({size_mb:.2f}MB)")
        print(f"  → Upload at: Customize → Skills → Add in the Claude Desktop app")


def main():
    parser = argparse.ArgumentParser(description="proof-of-creation skill installer")
    parser.add_argument("--skill", choices=list(SKILLS.keys()), help="Skill to install")
    parser.add_argument("--target", choices=list(TARGETS.keys()), default="claude-code", help="Target host")
    parser.add_argument("--project-dir", type=Path, help="Project directory for claude-project target")
    parser.add_argument("--force", action="store_true", help="Overwrite existing install without backup")
    parser.add_argument("--link", action="store_true", help="Symlink instead of copy (live edits)")
    parser.add_argument("--list", action="store_true", help="List available skills")
    args = parser.parse_args()

    if args.list:
        print("Available skills:")
        for name, info in SKILLS.items():
            print(f"  {name}: {info['description']}")
        return

    if not args.skill:
        parser.error("--skill is required (or use --list)")

    repo_root = Path(__file__).parent
    skill_info = SKILLS[args.skill]
    skill_path = repo_root / skill_info["path"]

    print(f"\n🛡️  proof-of-creation installer")
    print(f"   Skill: {args.skill}")
    print(f"   Target: {args.target}")

    # Validate
    print("\n→ Validating skill...")
    errors = validate_skill(skill_path)
    if errors:
        for e in errors:
            print(f"  ❌ {e}")
        sys.exit(1)
    print("  ✅ Validation passed")

    # Install
    print("\n→ Installing...")

    if args.target == "claude-code":
        config_dir = Path(os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude")).expanduser()
        target_dir = config_dir / "skills"
        target_dir.mkdir(parents=True, exist_ok=True)
        install_to_dir(skill_path, target_dir, args.skill, args.force, args.link)
        print(f"\n✅ Done! Invoke with /proof-of-creation in Claude Code.")
        print(f"   Run /skills to verify it loaded.")

    elif args.target == "claude-project":
        if not args.project_dir:
            parser.error("--project-dir required for claude-project target")
        target_dir = Path(args.project_dir) / ".claude" / "skills"
        target_dir.mkdir(parents=True, exist_ok=True)
        install_to_dir(skill_path, target_dir, args.skill, args.force, args.link)
        print(f"\n✅ Done! Commit .claude/skills/ to share with your repo.")

    elif args.target == "cowork":
        dist_dir = repo_root / "dist"
        print("\n→ Packaging for Cowork upload...")
        package_cowork(skill_path, args.skill, dist_dir)

    elif args.target == "cursor":
        target_dir = Path("~/.cursor/skills").expanduser()
        target_dir.mkdir(parents=True, exist_ok=True)
        install_to_dir(skill_path, target_dir, args.skill, args.force, args.link)
        print(f"\n✅ Done! Invoke with /proof-of-creation in Cursor.")


if __name__ == "__main__":
    main()
