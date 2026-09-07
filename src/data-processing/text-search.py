#!/usr/bin/env python3
"""Search extracted paper text for replication package links."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_DIR = REPO_ROOT / "all-papers-text"
DEFAULT_OUTPUT_FILE = REPO_ROOT / "results" / "replication-package-links.csv"

URL_PATTERN = re.compile(r"https?://[^\s<>()\"']+|www\.[^\s<>()\"']+", re.IGNORECASE)
REPLICATION_TERMS = (
    "replication package",
    "replication files",
    "replication material",
    "replication materials",
    "replication data",
    "artifact",
    "artifacts",
    "artefact",
    "artefacts",
    "artifact package",
    "artifact repository",
    "research artifact",
    "research artifacts",
    "supplementary material",
    "supplementary materials",
    "supplemental material",
    "supplemental materials",
    "source code",
    "computer code",
    "model code",
    "abm code",
    "code repository",
    "github repository",
    "git repository",
    "data repository",
    "codebase",
    "code base",
    "code can be downloaded",
    "code is available",
    "data are available",
    "data is available",
    "data availability",
)
REPOSITORY_HOSTS = (
    "github.com",
    "gitlab.com",
    "bitbucket.org",
    "zenodo.org",
    "figshare.com",
    "osf.io",
    "comses.net",
    "dataverse",
    "openicpsr",
    "mendeley.com/datasets",
)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def clean_url(url: str) -> str:
    return url.rstrip(".,;:)]}")


def extend_split_url(text: str, match: re.Match[str]) -> str:
    url = clean_url(match.group(0))
    cursor = match.end()

    while cursor < len(text):
        next_match = re.match(r"\s+(\S+)", text[cursor:])
        if not next_match:
            break

        token = next_match.group(1)
        fragment = token.rstrip(".,;:)]}")
        lower_url = url.lower()
        should_join = (
            lower_url in {"http://github", "https://github", "http://doi", "https://doi"}
            or url.endswith(("-", "/", "_"))
            or fragment.startswith((".", "/", "-", "_", "?", "#", "&", "="))
            or ("/" in fragment and any(host in lower_url for host in REPOSITORY_HOSTS))
        )

        if not fragment or not should_join:
            break

        url += fragment
        cursor += next_match.end()

        if token != fragment:
            break

    return clean_url(url)


def has_replication_context(context: str, url: str) -> bool:
    lower_context = context.lower()
    lower_url = url.lower()
    return any(term in lower_context for term in REPLICATION_TERMS) or any(
        host in lower_url for host in REPOSITORY_HOSTS
    )


def context_window(text: str, start: int, end: int, size: int = 160) -> str:
    context_start = max(0, start - size)
    context_end = min(len(text), end + size)
    return normalize_space(text[context_start:context_end])


def find_replication_links(txt_path: Path) -> list[dict[str, str]]:
    text = txt_path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"(https?)\s*:\s*/\s*/", r"\1://", text, flags=re.IGNORECASE)
    text = re.sub(r"(www)\s*\.", r"\1.", text, flags=re.IGNORECASE)
    matches = []

    for match in URL_PATTERN.finditer(text):
        url = extend_split_url(text, match)
        context = context_window(text, match.start(), match.end())

        if has_replication_context(context, url):
            matches.append(
                {
                    "paper": txt_path.stem,
                    "text_file": str(txt_path.relative_to(REPO_ROOT)),
                    "url": url,
                    "context": context,
                }
            )

    return matches


def write_results(rows: list[dict[str, str]], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["paper", "text_file", "url", "context"])
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search extracted paper text for replication package links."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Folder containing .txt files. Default: {DEFAULT_INPUT_DIR}",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
        help=f"CSV file for results. Default: {DEFAULT_OUTPUT_FILE}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.input_dir.exists():
        print(f"Input folder does not exist: {args.input_dir}")
        return 1

    rows = []
    for txt_path in sorted(args.input_dir.glob("*.txt")):
        rows.extend(find_replication_links(txt_path))

    write_results(rows, args.output_file)

    print(f"Scanned {len(list(args.input_dir.glob('*.txt')))} text file(s).")
    print(f"Found {len(rows)} possible replication package link(s).")
    print(f"Saved results to {args.output_file.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
