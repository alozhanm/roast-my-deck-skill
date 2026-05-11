"""PDF and text extraction with OCR fallback for image-based decks."""

from pathlib import Path

# Constants
MAX_TEXT_LENGTH = 50_000
MIN_TEXT_LENGTH = 100  # below this threshold the PDF is image-based → use OCR
WHITESPACE_CHARS = "\x00\x0b\x0c"
OCR_DPI = 150  # balance between quality and speed


def extract_from_pdf(path: str) -> str:
    """Extract text from a PDF, falling back to OCR for image-based decks.

    Args:
        path: Path to the PDF file.

    Returns:
        Extracted and cleaned text.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If no text can be extracted.
    """
    pdf_path = Path(path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    text = _try_text_extraction(pdf_path)

    if len(text.strip()) < MIN_TEXT_LENGTH:
        text = _try_ocr_extraction(pdf_path)

    if not text.strip():
        raise ValueError(f"No readable text found in '{path}'")

    return _clean_text(text)


def extract_from_text(text: str) -> str:
    """Clean and return raw pasted text.

    Args:
        text: Raw input string.

    Returns:
        Cleaned text string.
    """
    return _clean_text(text)


def _try_text_extraction(pdf_path: Path) -> str:
    """Attempt native text extraction via PyMuPDF.

    Args:
        pdf_path: Path to the PDF.

    Returns:
        Extracted text, or empty string on failure.
    """
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        pages = [page.get_text().strip() for page in doc if page.get_text().strip()]
        doc.close()
        return "\n\n".join(pages)
    except Exception:
        return ""


def _try_ocr_extraction(pdf_path: Path) -> str:
    """Render PDF pages as images and OCR them with easyocr.

    Uses PyMuPDF to render — no poppler/pdf2image dependency needed.

    Args:
        pdf_path: Path to the image-based PDF.

    Returns:
        OCR-extracted text.

    Raises:
        ValueError: If easyocr is not installed.
    """
    try:
        import easyocr
        import fitz
    except ImportError as e:
        raise ValueError(
            f"OCR dependency missing ({e}). Run: pip install easyocr pymupdf"
        ) from e

    reader = easyocr.Reader(["en"], verbose=False)
    doc = fitz.open(str(pdf_path))
    pages: list[str] = []

    for page in doc:
        mat = fitz.Matrix(OCR_DPI / 72, OCR_DPI / 72)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        results = reader.readtext(img_bytes, detail=0, paragraph=True)
        page_text = "\n".join(results).strip()
        if page_text:
            pages.append(page_text)

    doc.close()
    return "\n\n".join(pages)


def _clean_text(text: str) -> str:
    """Strip control characters and normalize whitespace.

    Args:
        text: Raw text to clean.

    Returns:
        Cleaned text truncated to MAX_TEXT_LENGTH.
    """
    for char in WHITESPACE_CHARS:
        text = text.replace(char, " ")
    lines = [line.strip() for line in text.splitlines()]
    cleaned = "\n".join(line for line in lines if line)
    return cleaned[:MAX_TEXT_LENGTH]
