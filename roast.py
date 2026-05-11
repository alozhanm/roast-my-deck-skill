"""Main entry point for roast-my-deck CLI."""

import sys

from src.extractor import extract_from_pdf, extract_from_text
from src.formatter import print_error, print_header, print_roast, print_success, print_warning
from src.roaster import load_context, roast

# Constants
CONTEXT_PATH = "context/successful_decks.txt"
PASTE_PROMPT = "Paste your pitch deck content below. Press Enter twice when done:\n"
PASTE_END_HINT = "(empty line ends input)"


def main() -> None:
    """Parse args and route to PDF or paste mode."""
    print_header()

    context = load_context(CONTEXT_PATH)
    if context:
        print_success("Loaded funded deck context — roast will be extra sharp.")
    else:
        print_warning("No context found. Run 'python3 ingest.py' to train on funded decks.")

    deck_text = _get_deck_text()
    if not deck_text:
        return

    print_success("Deck received. Sending to Claude for roasting...")
    try:
        response = roast(deck_text, context)
    except (ValueError, RuntimeError) as exc:
        print_error(str(exc))
        sys.exit(1)

    print_roast(response)


def _get_deck_text() -> str | None:
    """Return deck text from a PDF path arg or interactive paste mode.

    Returns:
        Extracted deck text, or None if extraction failed.
    """
    if len(sys.argv) > 1:
        return _load_from_pdf(sys.argv[1])
    return _load_from_paste()


def _load_from_pdf(path: str) -> str | None:
    """Extract text from a PDF file at the given path.

    Args:
        path: File system path to the PDF.

    Returns:
        Extracted text, or None on failure.
    """
    try:
        text = extract_from_pdf(path)
        print_success(f"Extracted text from '{path}'.")
        return text
    except (FileNotFoundError, ValueError) as exc:
        print_error(str(exc))
        return None


def _load_from_paste() -> str | None:
    """Read deck text from stdin until two consecutive newlines.

    Returns:
        Cleaned text, or None if nothing was entered.
    """
    print(PASTE_PROMPT)
    print(PASTE_END_HINT)
    lines: list[str] = []
    try:
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
    except (EOFError, KeyboardInterrupt):
        pass

    raw = "\n".join(lines).strip()
    if not raw:
        print_error("No content provided.")
        return None
    return extract_from_text(raw)


if __name__ == "__main__":
    main()
