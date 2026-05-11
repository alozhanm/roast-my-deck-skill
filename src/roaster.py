"""Claude API integration for pitch deck roasting."""

import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

# Constants
MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 1000
CONTEXT_HEADER = (
    "\n\nYou have studied the following real pitch decks that successfully raised "
    "funding. Use patterns from these decks to make your roast sharper and your "
    "fixes more specific:\n\n"
)
BASE_SYSTEM_PROMPT = """\
You are a brutally honest VC who has seen thousands of terrible pitch decks. \
You have zero patience and zero filter. You roast every deck like it's a comedy \
special. You swear. You mock vague mission statements, ridiculous TAM calculations, \
"Uber for X" ideas, and decks with zero traction. You're mean because you're right.

Structure your response exactly like this:

THE ROAST:
[Brutal roast, max 150 words, swearing allowed]

OK FINE, HERE'S HOW TO FIX IT:
1. [Specific actionable fix]
2. [Specific actionable fix]
3. [Specific actionable fix]\
"""


def load_context(context_path: str) -> str | None:
    """Load funded deck context from disk if it exists.

    Args:
        context_path: Path to the successful_decks.txt file.

    Returns:
        Context string if file exists and is non-empty, otherwise None.
    """
    path = Path(context_path)
    if not path.exists():
        return None
    content = path.read_text(encoding="utf-8").strip()
    return content if content else None


def build_system_prompt(context: str | None) -> str:
    """Construct the system prompt, optionally injecting funded deck context.

    Args:
        context: Funded deck text to inject, or None.

    Returns:
        Complete system prompt string.
    """
    if context:
        return BASE_SYSTEM_PROMPT + CONTEXT_HEADER + context
    return BASE_SYSTEM_PROMPT


def roast(deck_text: str, context: str | None = None) -> str:
    """Send the deck text to Claude and return the roast response.

    Args:
        deck_text: Extracted text from the pitch deck.
        context: Optional funded deck context string.

    Returns:
        Claude's roast response as a string.

    Raises:
        ValueError: If ANTHROPIC_API_KEY is not set.
        RuntimeError: If the API call fails.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key."
        )

    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = build_system_prompt(context)

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Here is the pitch deck to roast:\n\n{deck_text}",
                }
            ],
        )
    except anthropic.APIError as exc:
        raise RuntimeError(f"Claude API error: {exc}") from exc

    return message.content[0].text
