#!/usr/bin/env python3
"""Validate and atomically capture one sanitized experience from stdin."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import uuid


LOG_REL = Path("skills/skill-update/logs")
KINDS = {"user-correction", "verified-fix", "workflow-improvement", "observation"}
CONFIDENCES = {"verified", "user-stated", "unverified"}
TEXT_FIELDS = ("problem", "lesson", "action", "evidence", "scope")
SECRET_PATTERN = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    r"|\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"
    r"|\bsk-[A-Za-z0-9_-]{20,}"
    r"|(?:api[_-]?key|access[_-]?token|password|authorization)"
    r"""\s*["']?\s*[:=]\s*["']?(?:bearer\s+)?[A-Za-z0-9_./+=-]{12,}""",
    re.IGNORECASE,
)


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
    if git(repo, "ls-files", "--", str(LOG_REL)):
        raise ValueError("logs are tracked by Git; refuse to write")
    git(repo, "check-ignore", "-q", "--", str(LOG_REL / "events/probe.json"))
    return root


def nonempty(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")
    if len(value) > 8000:
        raise ValueError(f"{field} is too long; summarize instead of copying logs")
    return value.strip()


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    required = {"source", "topics", "kind", "confidence", *TEXT_FIELDS}
    if set(data) != required:
        raise ValueError(f"expected exactly these fields: {', '.join(sorted(required))}")
    source = data["source"]
    if not isinstance(source, dict) or set(source) - {"project", "session_id"}:
        raise ValueError("source must contain project and optional session_id")
    project = nonempty(source.get("project"), "source.project")
    session = source.get("session_id")
    if session is not None:
        session = nonempty(session, "source.session_id")
    topics = data["topics"]
    if not isinstance(topics, list) or not topics or len(topics) > 20:
        raise ValueError("topics must be a nonempty array of at most 20 strings")
    topics = sorted({nonempty(topic, "topic") for topic in topics})
    if not isinstance(data["kind"], str) or data["kind"] not in KINDS:
        raise ValueError("invalid kind")
    if not isinstance(data["confidence"], str) or data["confidence"] not in CONFIDENCES:
        raise ValueError("invalid confidence")
    if data["kind"] == "verified-fix" and data["confidence"] != "verified":
        raise ValueError("verified-fix requires verified confidence")
    if data["kind"] == "user-correction" and data["confidence"] == "unverified":
        raise ValueError("user-correction requires user-stated or verified confidence")
    result = {
        "source": {"project": project, "session_id": session},
        "topics": topics,
        "kind": data["kind"],
        "confidence": data["confidence"],
        **{field: nonempty(data[field], field) for field in TEXT_FIELDS},
    }
    if SECRET_PATTERN.search(json.dumps(result, ensure_ascii=False)):
        raise ValueError("possible secret detected; sanitize the experience first")
    return result


def write_event(root, data):
    # A persistent lock file is safe across process crashes; flock releases on exit.
    # No lock-file deletion, and no shared append to an events file.
    import fcntl

    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    events = root / "events"
    events.mkdir(exist_ok=True, mode=0o700)
    fingerprint = hashlib.sha256(
        json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    lock_fd = os.open(root / ".capture.lock", os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(lock_fd, "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in sorted(events.glob("*.json")):
            if path.is_symlink():
                raise ValueError(f"refuse symlinked event: {path.name}")
            existing = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(existing, dict) or existing.get("schema_version") != 1:
                raise ValueError(f"unsupported existing event: {path.name}")
            if existing.get("fingerprint") == fingerprint:
                if not isinstance(existing.get("id"), str):
                    raise ValueError(f"invalid existing event: {path.name}")
                return {"status": "duplicate", "id": existing["id"], "path": str(path)}
        now = datetime.now(timezone.utc)
        event_id = str(uuid.uuid4())
        event = {
            "schema_version": 1,
            "id": event_id,
            "recorded_at": now.isoformat(),
            "fingerprint": fingerprint,
            **data,
        }
        target = events / f"{now:%Y%m%dT%H%M%S%fZ}-{event_id}.json"
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=events, prefix=".event-", delete=False
            ) as handle:
                temporary = Path(handle.name)
                json.dump(event, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, target)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        return {"status": "recorded", "id": event_id, "path": str(target)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("~/Repos/lrac-skills"))
    args = parser.parse_args()
    try:
        # Resolve inbox before reading potentially large input; never create a repo.
        root = inbox(args.repo)
        raw = sys.stdin.read(65537)
        if len(raw) > 65536:
            raise ValueError("input exceeds 64 KiB; summarize the experience")
        result = write_event(root, validate(json.loads(raw)))
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Capture skipped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
