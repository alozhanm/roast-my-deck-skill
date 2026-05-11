"""Bulk ingestion of funded pitch decks for context building."""

import logging
from pathlib import Path

from src.extractor import extract_from_pdf

# Constants
DECK_HEADER_TEMPLATE = "=== DECK: {name} ==="
DECK_FOOTER = "=== END DECK ==="
SEPARATOR = "\n\n"

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def ingest_decks(decks_dir: str, output_path: str) -> int:
    """Scan all PDFs in decks_dir and write extracted text to output_path.

    Args:
        decks_dir: Directory containing funded deck PDFs.
        output_path: File path where aggregated context will be saved.

    Returns:
        Number of decks successfully ingested.
    """
    decks_path = Path(decks_dir)
    pdf_files = sorted(decks_path.glob("*.pdf"))

    if not pdf_files:
        logger.warning("No PDF files found in '%s'", decks_dir)
        return 0

    blocks: list[str] = []
    ingested = 0

    for pdf_file in pdf_files:
        block = _extract_deck_block(pdf_file)
        if block:
            blocks.append(block)
            ingested += 1

    if blocks:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(SEPARATOR.join(blocks), encoding="utf-8")

    return ingested


def _extract_deck_block(pdf_file: Path) -> str | None:
    """Extract text from a single PDF and wrap it in a deck block.

    Args:
        pdf_file: Path object pointing to the PDF.

    Returns:
        Formatted deck block string, or None if extraction failed.
    """
    try:
        text = extract_from_pdf(str(pdf_file))
        header = DECK_HEADER_TEMPLATE.format(name=pdf_file.name)
        return f"{header}\n{text}\n\n{DECK_FOOTER}"
    except (FileNotFoundError, ValueError) as exc:
        logger.warning("Skipping '%s': %s", pdf_file.name, exc)
        return None
