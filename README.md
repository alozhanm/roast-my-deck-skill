# roast-my-deck 🔥

A CLI tool that brutally roasts your pitch deck using Claude, trained on real funded decks.

Also ships as a `/roast` skill for Claude Code — no API key needed.

---

## quickstart (2 minutes)

```bash
git clone https://github.com/alizhannurgazy/roast-my-deck-skill
cd roast-my-deck-skill
bash install.sh
```

That's it. The repo ships with context from 12 real funded decks ($1.3M–$22M raised). You're ready to roast immediately.

---

## usage

### option A — Claude Code skill (recommended, free, no API key)

After running `install.sh`, use `/roast` in **any** Claude Code session:

```bash
/roast deck.pdf       # roast a PDF
/roast                # paste your deck manually
```

Works from any directory. Claude reads your deck visually (handles image-based PDFs from Figma, Canva, Google Slides) and roasts it using context from real funded decks.

### option B — CLI tool (requires Anthropic API key)

```bash
cp .env.example .env
# add your ANTHROPIC_API_KEY to .env
# get your key at console.anthropic.com (~$0.003 per roast)

python3 roast.py deck.pdf   # roast a PDF
python3 roast.py            # paste mode, press Enter twice to submit
```

---

## add your own funded decks

Drop PDF pitch decks into the `decks/` folder, then:

```bash
python3 ingest.py
```

This extracts the text and updates `context/successful_decks.txt`. Both the skill and CLI load this context automatically — the more funded decks you add, the sharper the roasts.

The repo ships with 12 pre-ingested funded decks:

| Company | Round | Raised |
|---|---|---|
| Candidate.fyi | Pre-Seed | $1.3M |
| Cerebrium (YC W22) | Seed | $8.5M |
| ElevenLabs | Pre-Seed | $2M |
| Gradient Labs | Series A | $13M |
| Lago (YC S21) | Seed | $22M |
| Malibou (YC W24) | Seed | $3.3M |
| Pathrise (YC S17) | Seed | $3M |
| Recall | Series A | $10M |
| Series | Pre-Seed | $3M |
| Tiun | Pre-Seed | $2.5M |
| Smartrr | Series A | $10M |
| Storiaverse | Pre-Seed | $2.5M |

> PDFs are not in the repo (copyright). Only the extracted text context is committed.

---

## how it works

```
your deck (PDF or paste)
        ↓
   text extraction (PyMuPDF)
   or visual rendering for image-based PDFs
        ↓
   funded deck context (context/successful_decks.txt)
        ↓
   brutal foul-mouthed VC persona (Claude AI)
        ↓
   roast + 3 actionable fixes
```

---

## project structure

```
roast-my-deck-skill/
├── src/
│   ├── extractor.py      PDF text extraction + OCR fallback
│   ├── ingestor.py       bulk deck ingestion
│   ├── roaster.py        Claude API calls (CLI mode)
│   └── formatter.py      terminal output formatting
├── skill/
│   └── SKILL.md          /roast skill for Claude Code
├── context/
│   └── successful_decks.txt   pre-ingested funded deck context
├── decks/
│   └── .gitkeep          drop your funded PDFs here (gitignored)
├── tests/
│   └── test_roaster.py
├── roast.py              CLI entry point
├── ingest.py             ingestion entry point
└── install.sh            one-command setup
```

---

## contributing

PRs welcome:
- Add more funded decks: drop PDFs in `decks/`, run `python3 ingest.py`, commit `context/successful_decks.txt`
- Better OCR for image-based PDFs
- More roast personas (angels, accelerators, corporate VCs)

---

## stack

- Python 3.10+
- [Claude Sonnet](https://anthropic.com) — CLI mode
- [Claude Code](https://claude.ai/code) skill — `/roast` mode (no API key)
- [PyMuPDF](https://pymupdf.readthedocs.io) — PDF extraction
- [Colorama](https://github.com/tartley/colorama) — terminal colors

---

## license

MIT
