#!/usr/bin/env python3

import argparse
import datetime
import json
import os
import subprocess
import zipfile
from pathlib import Path


DEFAULT_WORKSPACE_REPOS = [
    r"C:\Users\nazmi\QuantumAvatar",
    r"C:\Users\nazmi\gdp-dashboard",
    r"C:\Users\nazmi\NeCUsersLaptopDocumentsCCashMoneyIDEKontrollzentrumuer-Ordner",
    r"C:\Users\nazmi\-MEGA-ULTRA-ROBOTER-KI",
    r"C:\Users\nazmi\-MEGA-ULTRA-ROBOTER-KI-1",
    r"C:\Users\nazmi\mega_app_launcher.py",
    r"C:\Users\nazmi\blank-app",
    r"C:\Users\nazmi\blank-app-1",
    r"C:\Users\nazmi\blank-app-2",
    r"C:\Users\nazmi\AutonomousZenithOptimizer",
    r"C:\Users\nazmi\AutonomousZenithOptimizer-1",
    r"C:\Users\nazmi\modules",
    r"C:\Users\nazmi\desktop-tutorial",
    r"C:\Users\nazmi\Mega-Umgebung",
    r"C:\Users\nazmi\Mega-Umgebung-1",
    r"C:\Users\nazmi\Documents-1",
    r"C:\Users\nazmi\Kontrollzentrum",
]


def _timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_folder_name(path: Path) -> str:
    name = path.name
    return "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in name)


def _run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    except FileNotFoundError as exc:
        return subprocess.CompletedProcess(cmd, 127, "", str(exc))


def _is_git_repo(repo_path: Path) -> bool:
    return (repo_path / ".git").exists()


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _zip_tree(
    source_dir: Path,
    zip_path: Path,
    *,
    exclude_dir_names: set[str],
    exclude_top_level_names: set[str],
) -> dict:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    files_count = 0
    bytes_count = 0

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
        for root, dirs, files in os.walk(source_dir):
            root_path = Path(root)
            rel_root = root_path.relative_to(source_dir)

            # Exclude top-level folders/files (avoid recursion into the backup output itself).
            if rel_root.parts and rel_root.parts[0] in exclude_top_level_names:
                dirs[:] = []
                continue

            # Prune directory traversal.
            dirs[:] = [d for d in dirs if d not in exclude_dir_names]

            for filename in files:
                file_path = root_path / filename
                try:
                    rel_path = file_path.relative_to(source_dir)
                except ValueError:
                    continue

                if rel_path.parts and rel_path.parts[0] in exclude_top_level_names:
                    continue

                try:
                    st = file_path.stat()
                    bytes_count += st.st_size
                except OSError:
                    continue

                zipf.write(file_path, arcname=str(rel_path))
                files_count += 1

    return {"zip": str(zip_path), "files": files_count, "bytes": bytes_count}


def _export_vscode_extensions(out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    candidates = [
        ["code", "--list-extensions", "--show-versions"],
        ["code-insiders", "--list-extensions", "--show-versions"],
        ["code.cmd", "--list-extensions", "--show-versions"],
        ["code-insiders.cmd", "--list-extensions", "--show-versions"],
    ]

    for cmd in candidates:
        proc = _run(cmd)
        if proc.returncode == 0 and proc.stdout.strip():
            target = out_dir / "vscode_extensions.txt"
            _write_text(target, proc.stdout)
            return {"ok": True, "command": " ".join(cmd), "output": str(target)}

    return {"ok": False, "error": "VS Code CLI nicht gefunden (code/insiders nicht im PATH)."}


def backup_repo(repo_path: Path, out_root: Path, *, make_zip: bool, make_git: bool) -> dict:
    repo_path = repo_path.resolve()
    repo_name = _safe_folder_name(repo_path)
    repo_out = out_root / repo_name
    repo_out.mkdir(parents=True, exist_ok=True)

    result: dict = {
        "repo": str(repo_path),
        "out": str(repo_out),
        "zip": None,
        "git": None,
        "errors": [],
    }

    if make_zip:
        exclude_dirs = {"__pycache__"}
        exclude_top_level = {"backups"}
        # Do not zip .git; the git bundle is the canonical source backup.
        exclude_dirs.add(".git")
        zip_path = repo_out / f"{repo_name}_working_tree.zip"
        try:
            result["zip"] = _zip_tree(
                repo_path,
                zip_path,
                exclude_dir_names=exclude_dirs,
                exclude_top_level_names=exclude_top_level,
            )
        except Exception as exc:
            result["errors"].append(f"zip_failed: {exc}")

    if make_git and _is_git_repo(repo_path):
        bundle_path = repo_out / f"{repo_name}.bundle"
        status_path = repo_out / "git-status.txt"
        head_path = repo_out / "HEAD.txt"
        diff_path = repo_out / "working-tree.patch"
        diff_cached_path = repo_out / "index.patch"

        try:
            head = _run(["git", "-C", str(repo_path), "rev-parse", "HEAD"])
            _write_text(head_path, head.stdout.strip() + "\n" if head.returncode == 0 else "(unknown)\n")

            status = _run(["git", "-C", str(repo_path), "status", "--porcelain"])
            _write_text(status_path, status.stdout)

            diff = _run(["git", "-C", str(repo_path), "diff"])
            _write_text(diff_path, diff.stdout)

            diff_cached = _run(["git", "-C", str(repo_path), "diff", "--cached"])
            _write_text(diff_cached_path, diff_cached.stdout)

            bundle = _run(["git", "-C", str(repo_path), "bundle", "create", str(bundle_path), "--all"])
            if bundle.returncode != 0 or not bundle_path.exists():
                result["errors"].append(f"bundle_failed: {bundle.stderr.strip() or bundle.stdout.strip()}")
                result["git"] = {"bundle": None}
            else:
                result["git"] = {
                    "bundle": str(bundle_path),
                    "status": str(status_path),
                    "head": str(head_path),
                    "working_tree_patch": str(diff_path),
                    "index_patch": str(diff_cached_path),
                }
        except Exception as exc:
            result["errors"].append(f"git_backup_failed: {exc}")
    elif make_git:
        result["git"] = {"bundle": None, "note": "Kein Git-Repo (.git fehlt)"}

    return result


def create_backup(
    *,
    output_root: Path,
    repos: list[Path],
    include_all_repos: bool,
    make_zip: bool,
    make_git: bool,
) -> Path:
    ts = _timestamp()
    out_root = output_root / ts
    out_root.mkdir(parents=True, exist_ok=False)

    selected_repos = repos if include_all_repos else [Path.cwd()]
    selected_repos = [Path(p) for p in selected_repos]
    selected_repos = [p for p in selected_repos if p.exists()]

    meta_dir = out_root / "_meta"
    meta_dir.mkdir(parents=True, exist_ok=True)

    vscode_info = _export_vscode_extensions(meta_dir)

    results = []
    for repo_path in selected_repos:
        results.append(backup_repo(repo_path, out_root, make_zip=make_zip, make_git=make_git))

    manifest = {
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "output_root": str(out_root),
        "make_zip": make_zip,
        "make_git": make_git,
        "repos": results,
        "vscode": vscode_info,
    }
    (out_root / "BACKUP_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Human-readable summary
    lines = [
        f"Backup erstellt: {out_root}",
        f"Repos: {len(results)}",
        f"ZIP: {'on' if make_zip else 'off'} | Git bundle+patches: {'on' if make_git else 'off'}",
        f"VS Code Extensions: {'ok' if vscode_info.get('ok') else 'n/a'}",
        "",
    ]
    for r in results:
        repo = r.get("repo")
        errs = r.get("errors") or []
        lines.append(f"- {repo}")
        if r.get("zip"):
            z = r["zip"]
            lines.append(f"  zip: {z.get('zip')} ({z.get('files')} files)")
        if r.get("git"):
            g = r["git"]
            lines.append(f"  git: {g.get('bundle') or 'none'}")
        if errs:
            lines.append(f"  errors: {', '.join(errs)}")
    _write_text(out_root / "BACKUP_SUMMARY.txt", "\n".join(lines) + "\n")

    return out_root


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Erstellt einen neuen Backup-Snapshot (kein Überschreiben): "
            "ZIP-Working-Tree + optional Git-Bundles & Patches pro Repo."
        )
    )
    parser.add_argument(
        "--output-root",
        default=r"C:\Users\nazmi\BACKUPS",
        help="Ziel-Root-Ordner für Backups (Standard: C:\\Users\\nazmi\\BACKUPS)",
    )
    parser.add_argument(
        "--all-repos",
        action="store_true",
        help="Backup für alle bekannten Workspace-Repos (Default, wenn gesetzt)",
    )
    parser.add_argument(
        "--repo",
        action="append",
        default=[],
        help="Zusätzlicher Repo-Pfad (kann mehrfach angegeben werden)",
    )
    parser.add_argument(
        "--no-zip",
        action="store_true",
        help="Kein ZIP-Working-Tree erstellen",
    )
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Keine Git-Bundles/Patches erstellen",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    # Default: wir sichern alles (kein Überschreiben, immer neuer Timestamp-Ordner).
    include_all_repos = True

    repos = [Path(p) for p in DEFAULT_WORKSPACE_REPOS]
    repos.extend(Path(p) for p in args.repo)

    make_zip = not args.no_zip
    make_git = not args.no_git

    out_dir = create_backup(
        output_root=output_root,
        repos=repos,
        include_all_repos=include_all_repos,
        make_zip=make_zip,
        make_git=make_git,
    )
    print(f"Backup erstellt: {out_dir}")
    print(f"Summary: {out_dir / 'BACKUP_SUMMARY.txt'}")
    print(f"Manifest: {out_dir / 'BACKUP_MANIFEST.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
