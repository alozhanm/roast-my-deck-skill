"""Entry point for ingesting funded pitch decks."""

import sys

from src.formatter import print_error, print_success, print_warning
from src.ingestor import ingest_decks

# Constants
DECKS_DIR = "decks"
OUTPUT_PATH = "context/successful_decks.txt"


def main() -> None:
    """Ingest all PDFs from the decks/ folder and report results."""
    print_success("Scanning decks/ folder for funded pitch decks...")

    try:
        count = ingest_decks(DECKS_DIR, OUTPUT_PATH)
    except Exception as exc:  # noqa: BLE001
        print_error(f"Ingestion failed: {exc}")
        sys.exit(1)

    if count == 0:
        print_warning(
            "No decks ingested. Drop PDF files into the decks/ folder and try again."
        )
    else:
        print_success(
            f"Ingested {count} deck{'s' if count != 1 else ''} → {OUTPUT_PATH}"
        )
        print_success("Run 'python roast.py' to use the sharpened context.")


if __name__ == "__main__":
    main()
