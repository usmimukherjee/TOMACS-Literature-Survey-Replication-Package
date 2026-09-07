#!/usr/bin/env python3
"""Extract text from every PDF in all-papers and save one .txt file per PDF."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        PdfReader = None


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_DIR = REPO_ROOT / "all-papers"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "all-papers-text"


def sanitize_filename(value: str, fallback: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", value).strip()
    value = re.sub(r"\s+", " ", value)
    value = value.rstrip(". ")
    return value[:180] or fallback


def unique_output_path(output_dir: Path, stem: str) -> Path:
    output_path = output_dir / f"{stem}.txt"
    counter = 2

    while output_path.exists():
        output_path = output_dir / f"{stem} ({counter}).txt"
        counter += 1

    return output_path


def extract_pdf_text_and_title(pdf_path: Path) -> tuple[str, str | None]:
    if PdfReader is None:
        raise RuntimeError(
            "Missing PDF dependency. Install one with: python3 -m pip install pypdf"
        )

    reader = PdfReader(str(pdf_path))
    pages = []
    title = None

    if reader.metadata and reader.metadata.title:
        title = str(reader.metadata.title).strip()

    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages.append(text.strip())

    return "\n\n".join(pages).strip(), title


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def extract_pdf_to_text(pdf_path: Path, output_dir: Path) -> Path:
    text, title = extract_pdf_text_and_title(pdf_path)
    output_stem = sanitize_filename(title or pdf_path.stem, pdf_path.stem)
    output_path = unique_output_path(output_dir, output_stem)
    output_path.write_text(text + "\n", encoding="utf-8")
    return output_path


def extract_pdf_paths(pdf_paths: list[Path], output_dir: Path) -> tuple[int, int]:
    output_dir.mkdir(parents=True, exist_ok=True)

    if not pdf_paths:
        print("No PDF files found.")
        return 0, 0

    successful = 0
    failed = 0

    for pdf_path in pdf_paths:
        try:
            output_path = extract_pdf_to_text(pdf_path, output_dir)
            successful += 1
            print(f"Extracted: {pdf_path.name} -> {display_path(output_path)}")
        except Exception as exc:
            failed += 1
            print(f"Failed: {pdf_path.name}: {exc}", file=sys.stderr)

    return successful, failed


def extract_all_pdfs(input_dir: Path, output_dir: Path) -> tuple[int, int]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input folder does not exist: {input_dir}")

    return extract_pdf_paths(sorted(input_dir.glob("*.pdf")), output_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract text from PDF files and save matching .txt files."
    )
    parser.add_argument(
        "--pdf-file",
        type=Path,
        help="Extract a single PDF file instead of every PDF in the input folder.",
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Folder containing PDF files. Default: {DEFAULT_INPUT_DIR}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Folder for extracted .txt files. Default: {DEFAULT_OUTPUT_DIR}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if args.pdf_file:
            if not args.pdf_file.exists():
                raise FileNotFoundError(f"PDF file does not exist: {args.pdf_file}")
            successful, failed = extract_pdf_paths([args.pdf_file], args.output_dir)
        else:
            successful, failed = extract_all_pdfs(args.input_dir, args.output_dir)
    except Exception as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"Done. Extracted {successful} PDF(s); {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
