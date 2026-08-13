#!/usr/bin/env python3
"""Run local structural and parser smoke checks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"


def main() -> int:
    for skill in sorted((ROOT / "skills").iterdir()):
        subprocess.run([sys.executable, str(VALIDATOR), str(skill)], check=True)

    fixture = ROOT / "tests/fixtures/xiaoyuzhou.html"
    extractor = ROOT / "skills/xiaoyuzhou-media/scripts/extract_xiaoyuzhou.py"
    result = subprocess.run(
        [
            sys.executable,
            str(extractor),
            "https://www.xiaoyuzhoufm.com/episode/1234567890abcdef12345678",
            "--html",
            str(fixture),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)["data"]
    assert data["title"] == "测试节目"
    assert data["audio_url"] == "https://media.xyzcdn.net/test.m4a"
    assert data["duration_seconds"] == 754
    assert data["subscriber_count"] == 42
    print("All validation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
