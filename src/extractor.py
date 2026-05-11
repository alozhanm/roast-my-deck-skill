"""PDF and text extraction utilities."""

from pathlib import Path

# Constants
MAX_TEXT_LENGTH = 50_000
WHITESPACE_CHARS = "\x00\x0b\x0c"


def extract_from_pdf(path: str) -> str:
    """Extract text from a PDF file using PyMuPDF.

    Args:
        path: Absolute or relative path to the PDF file.

    Returns:
        Extracted and cleaned text content.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ValueError: If the file cannot be read or contains no text.
    """
    import fitz  # PyMuPDF

    pdf_path = Path(path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    try:
        doc = fitz.open(str(pdf_path))
    except Exception as exc:
        raise ValueError(f"Cannot open PDF '{path}': {exc}") from exc

    pages: list[str] = []
    for page in doc:
        text = page.get_text()
        if text.strip():
            pages.append(text.strip())
    doc.close()

    if not pages:
        raise ValueError(f"No readable text found in '{path}'")

    combined = "\n\n".join(pages)
    return _clean_text(combined)


def extract_from_text(text: str) -> str:
    """Clean and return raw pasted text.

    Args:
        text: Raw string input from the user.

    Returns:
        Cleaned text string.
    """
    return _clean_text(text)


def _clean_text(text: str) -> str:
    """Normalize whitespace and strip control characters.

    Args:
        text: Raw text to clean.

    Returns:
        Cleaned text, truncated to MAX_TEXT_LENGTH.
    """
    for char in WHITESPACE_CHARS:
        text = text.replace(char, " ")
    lines = [line.strip() for line in text.splitlines()]
    cleaned = "\n".join(line for line in lines if line)
    return cleaned[:MAX_TEXT_LENGTH]
