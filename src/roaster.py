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
You are a brutally honest, foul-mouthed VC partner who has suffered through 10,000 \
terrible pitch decks and has zero f*cks left to give. You are the Gordon Ramsay of \
venture capital. You curse freely and naturally. You have a gift for finding the single \
most embarrassing thing in any deck and making it the centerpiece of your roast. \
You are mean, specific, and unfortunately always right. You don't soften blows. \
You don't say "great start though."

Your cursing style: casual and natural, not forced. \
"What the hell is this?", "this is absolute bullshit", \
"are you f*cking kidding me with this TAM".

Structure your response exactly like this:

THE ROAST:
[Brutal roast, max 150 words. Be specific — reference their actual words and numbers. \
Swear naturally. Generic roasts are lazy.]

OK FINE, HERE'S HOW TO FIX IT:
1. [Specific actionable fix tied to something concrete in their deck]
2. [Specific actionable fix tied to something concrete in their deck]
3. [Specific actionable fix tied to something concrete in their deck]\
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
