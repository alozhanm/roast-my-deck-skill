#!/usr/bin/env bash
set -e

SKILL_DIR="$HOME/.claude/skills/roast"

echo "🔥 Installing roast-my-deck..."

# Dependencies
echo "→ Installing Python dependencies..."
pip3 install -q -r requirements.txt

# .env
if [ ! -f .env ]; then
  cp .env.example .env
  echo "→ Created .env — add your ANTHROPIC_API_KEY if using the CLI tool."
fi

# Claude Code skill
if command -v claude &>/dev/null || [ -d "$HOME/.claude" ]; then
  echo "→ Installing /roast skill for Claude Code..."
  mkdir -p "$SKILL_DIR"
  cp skill/SKILL.md "$SKILL_DIR/SKILL.md"
  echo "  ✓ Skill installed. Use /roast in any Claude Code session."
else
  echo "  ⚠ Claude Code not detected — skipping skill install."
  echo "    To install manually: mkdir -p $SKILL_DIR && cp skill/SKILL.md $SKILL_DIR/"
fi

echo ""
echo "✓ Done. Usage:"
echo "  python3 roast.py deck.pdf   # roast a PDF (needs API key in .env)"
echo "  python3 roast.py            # paste mode"
echo "  python3 ingest.py           # ingest funded decks from decks/"
echo "  /roast deck.pdf             # inside Claude Code (no API key needed)"
