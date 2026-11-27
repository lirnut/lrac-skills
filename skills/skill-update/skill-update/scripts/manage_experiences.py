#!/usr/bin/env python3
"""List captured experiences and append local review decisions. Never edit Git."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import uuid


LOG_REL = Path("skills/skill-update/logs")


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], text=True, capture_output=True, check=True
    ).stdout.strip()


def inbox(repo):
    repo = repo.expanduser().resolve()
    if not (repo / ".git").exists():
        raise ValueError("central repository does not exist or has no .git")
    if Path(git(repo, "rev-parse", "--show-toplevel")).resolve() != repo:
        raise ValueError("--repo must point to the central repository root")
    for name in ("skill-update", "skill-expcap"):
        if not (repo / "skills/skill-update" / name / "SKILL.md").is_file():
            raise ValueError(f"central repository is missing {name}/SKILL.md")
    root = repo / LOG_REL
    for path in (root, root / "events", root / "applications"):
        if path.resolve() != path:
            raise ValueError("log paths must not contain symlinks")
        if path.exists() and not path.is_dir():
            raise ValueError(f"log path is not a directory: {path}")
    return repo, root


def read_records(directory):
    records = []
    for path in sorted(directory.glob("*.json")):
        if path.is_symlink():
            raise ValueError(f"refuse symlinked log: {path.name}")
        item = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(item, dict) or item.get("schema_version") != 1:
            raise ValueError(f"unsupported record: {path.name}")
        if not isinstance(item.get("id"), str) or not isinstance(item.get("recorded_at"), str):
            raise ValueError(f"invalid record identity: {path.name}")
        records.append(item)
    return sorted(records, key=lambda item: (item["recorded_at"], item["id"]))


def decisions(root):
    latest = {}
    for record in read_records(root / "applications"):
        if record.get("decision") not in {"pending", "applied", "deferred", "rejected"}:
            raise ValueError("invalid application decision")
        ids = record.get("event_ids")
        if not isinstance(ids, list) or not all(isinstance(i, str) for i in ids):
            raise ValueError("invalid application event_ids")
        for event_id in ids:
            latest[event_id] = record
    return latest


def list_events(root, args):
    latest = decisions(root)
    result = []
    for event in read_records(root / "events"):
        application = latest.get(event["id"])
        state = application["decision"] if application else "pending"
        if not args.all and state not in {"pending", "deferred"}:
            continue
        if args.topic and args.topic not in event.get("topics", []):
            continue
        result.append({"event": event, "decision": state, "application": application})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record_decision(repo, root, args):
    if git(repo, "ls-files", "--", str(LOG_REL)):
        raise ValueError("logs are tracked by Git; refuse to write")
    git(repo, "check-ignore", "-q", "--", str(LOG_REL / "applications/probe.json"))
    available = {event["id"] for event in read_records(root / "events")}
    missing = set(args.event) - available
    if missing:
        raise ValueError(f"unknown event IDs: {', '.join(sorted(missing))}")
    if not args.reason.strip() or len(args.reason) > 8000:
        raise ValueError("provide a concise nonempty reason")
    commit = args.commit
    if args.decision == "applied":
        if not args.branch or not commit:
            raise ValueError("applied requires --branch and --commit")
        if not args.branch.startswith("feat/") or not args.branch.endswith("-skill"):
            raise ValueError("expected feat/<skill>-skill branch")
        git(repo, "check-ref-format", "--branch", args.branch)
        if not re.fullmatch(r"[a-fA-F0-9]{40}|[a-fA-F0-9]{64}", commit):
            raise ValueError("--commit must be a full commit hash")
        commit = git(repo, "rev-parse", "--verify", f"{commit}^{{commit}}")
        git(repo, "merge-base", "--is-ancestor", commit, f"refs/heads/{args.branch}")
    elif args.branch or commit:
        raise ValueError("branch and commit are only valid for applied decisions")
    now = datetime.now(timezone.utc)
    record_id = str(uuid.uuid4())
    record = {
        "schema_version": 1,
        "id": record_id,
        "recorded_at": now.isoformat(),
        "event_ids": sorted(set(args.event)),
        "decision": args.decision,
        "reason": args.reason.strip(),
        "branch": args.branch,
        "commit": commit,
    }
    directory = root / "applications"
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    target = directory / f"{now:%Y%m%dT%H%M%S%fZ}-{record_id}.json"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=directory, prefix=".application-", delete=False
        ) as handle:
            temporary = Path(handle.name)
            json.dump(record, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(json.dumps({"status": "recorded", "path": str(target)}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("~/Repos/lrac-skills"))
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="list pending and deferred events")
    listing.add_argument("--all", action="store_true")
    listing.add_argument("--topic")
    recording = commands.add_parser("record", help="append a decision without touching events")
    recording.add_argument("--event", action="append", required=True)
    recording.add_argument(
        "--decision", required=True, choices=("pending", "applied", "deferred", "rejected")
    )
    recording.add_argument("--reason", required=True)
    recording.add_argument("--branch")
    recording.add_argument("--commit")
    args = parser.parse_args()
    try:
        repo, root = inbox(args.repo)
        if args.command == "list":
            list_events(root, args)
        else:
            record_decision(repo, root, args)
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Experience operation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
