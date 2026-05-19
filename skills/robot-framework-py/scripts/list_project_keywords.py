#!/usr/bin/env python3
"""List all Robot Framework user keywords in this project.

The script scans .robot and .resource files, extracts keyword definitions from
"*** Keywords ***" sections, and prints where each keyword is defined.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, List, Tuple

SECTION_HEADER_RE = re.compile(r"^\*{3}\s*([^*]+?)\s*\*{3}\s*$", re.IGNORECASE)

DEFAULT_EXCLUDES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "logs",
    "results",
    "__pycache__",
    "iih-test-runner",
}

DEFAULT_SCAN_DIRS = [
    "common",
    "test/robotframework/resources",
]


def is_section_header(line: str) -> bool:
    return bool(SECTION_HEADER_RE.match(line.strip()))


def parse_section_name(line: str) -> str:
    match = SECTION_HEADER_RE.match(line.strip())
    return match.group(1).strip().lower() if match else ""


def extract_keywords(file_path: Path) -> List[Tuple[str, int]]:
    keywords: List[Tuple[str, int]] = []
    in_keywords_section = False

    for line_number, raw_line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw_line.strip()

        if is_section_header(raw_line):
            in_keywords_section = parse_section_name(raw_line) == "keywords"
            continue

        if not in_keywords_section:
            continue

        if not stripped:
            continue

        if stripped.startswith("#"):
            continue

        # In Robot files, keyword declarations are top-level lines in the
        # Keywords section. Step lines are indented.
        if raw_line.startswith((" ", "\t")):
            continue

        if stripped.startswith(("[", "...")):
            continue

        keywords.append((stripped, line_number))

    return keywords


def should_skip(path: Path) -> bool:
    return any(part in DEFAULT_EXCLUDES for part in path.parts)


def collect_keywords(root: Path, scan_dirs: List[str]) -> Dict[str, List[Tuple[str, int]]]:
    keyword_map: Dict[str, List[Tuple[str, int]]] = {}

    for scan_dir in scan_dirs:
        scan_path = (root / scan_dir).resolve()
        if not scan_path.exists() or not scan_path.is_dir():
            continue

        for file_path in scan_path.rglob("*"):
            if file_path.suffix not in {".robot", ".resource"}:
                continue
            if should_skip(file_path):
                continue

            for name, line_number in extract_keywords(file_path):
                rel_path = file_path.relative_to(root).as_posix()
                keyword_map.setdefault(name, []).append((rel_path, line_number))

    return keyword_map


def group_locations_by_scan_dir(
    keyword_map: Dict[str, List[Tuple[str, int]]], scan_dirs: List[str]
) -> Dict[str, Dict[str, List[Tuple[str, int]]]]:
    grouped: DefaultDict[str, Dict[str, List[Tuple[str, int]]]] = defaultdict(dict)
    normalized_dirs = [(d, d.strip("/")) for d in scan_dirs]

    for name, locations in keyword_map.items():
        for path, line in locations:
            matched_group = "others"
            for display_name, normalized in normalized_dirs:
                if path == normalized or path.startswith(f"{normalized}/"):
                    matched_group = display_name
                    break

            grouped[matched_group].setdefault(name, []).append((path, line))

    return dict(grouped)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="List Robot Framework keywords in project files.")
    parser.add_argument("--root", default=".", help="Project root path to scan. Default: current directory")
    parser.add_argument(
        "--scan-dir",
        action="append",
        default=None,
        help=(
            "Directory to scan under root. Repeatable. "
            "Default: common and test/robotframework/resources"
        ),
    )
    parser.add_argument("--json", action="store_true", dest="as_json", help="Print output in JSON format")
    parser.add_argument(
        "--only-duplicates",
        action="store_true",
        help="Print only keywords that are defined in more than one file/location",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional output file path. If omitted, prints to stdout.",
    )
    return parser


def render_text(
    keyword_map: Dict[str, List[Tuple[str, int]]],
    only_duplicates: bool,
    scan_dirs: List[str],
) -> str:
    lines: List[str] = []
    all_definitions = sum(len(locations) for locations in keyword_map.values())
    grouped = group_locations_by_scan_dir(keyword_map, scan_dirs)

    lines.append(f"Total keyword definitions: {all_definitions}")
    lines.append(f"Total unique keywords: {len(keyword_map)}")
    lines.append(f"Scanned directories: {', '.join(scan_dirs)}")
    lines.append("")

    for group_name in scan_dirs:
        group_keywords = grouped.get(group_name, {})
        group_definitions = sum(len(v) for v in group_keywords.values())
        lines.append(f"[{group_name}] definitions={group_definitions}, unique={len(group_keywords)}")

        sorted_names = sorted(group_keywords.keys(), key=lambda x: x.lower())
        for name in sorted_names:
            locations = group_keywords[name]
            if only_duplicates and len(keyword_map.get(name, [])) < 2:
                continue

            loc_text = ", ".join(f"{path}:{line}" for path, line in locations)
            lines.append(f"{name}\t{loc_text}")

        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_json(
    keyword_map: Dict[str, List[Tuple[str, int]]],
    only_duplicates: bool,
    scan_dirs: List[str],
) -> str:
    grouped = group_locations_by_scan_dir(keyword_map, scan_dirs)
    payload = {
        "summary": {
            "total_keyword_definitions": sum(len(v) for v in keyword_map.values()),
            "total_unique_keywords": len(keyword_map),
            "scan_dirs": scan_dirs,
        },
        "groups": {},
    }

    for group_name in scan_dirs:
        group_keywords = grouped.get(group_name, {})
        group_payload = {
            "summary": {
                "total_keyword_definitions": sum(len(v) for v in group_keywords.values()),
                "total_unique_keywords": len(group_keywords),
            },
            "keywords": {},
        }

        for name in sorted(group_keywords.keys(), key=lambda x: x.lower()):
            locations = group_keywords[name]
            if only_duplicates and len(keyword_map.get(name, [])) < 2:
                continue

            group_payload["keywords"][name] = [
                {"file": path, "line": line_number} for path, line_number in locations
            ]

        payload["groups"][group_name] = group_payload

    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    root = Path(args.root).resolve()
    scan_dirs = args.scan_dir if args.scan_dir else DEFAULT_SCAN_DIRS
    keyword_map = collect_keywords(root, scan_dirs)

    output = (
        render_json(keyword_map, args.only_duplicates, scan_dirs)
        if args.as_json
        else render_text(keyword_map, args.only_duplicates, scan_dirs)
    )

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
