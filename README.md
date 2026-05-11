# roast-my-deck 🔥

A CLI tool that brutally roasts your pitch deck using Claude AI, trained on real funded decks.

Also ships as a `/roast` skill for Claude Code — no API key needed.

---

## quickstart (2 minutes)

```bash
git clone https://github.com/yourusername/roast-my-deck
cd roast-my-deck
bash install.sh
```

That's it. The repo already includes context from 12 real funded decks ($1.3M–$22M raised). You're ready to roast.

---

## usage

### option A — Claude Code skill (recommended, no API key)

Open Claude Code in the project directory:

```bash
/roast deck.pdf       # roast a PDF
/roast                # paste your deck manually
```

Claude roasts it directly. Free, instant, no setup beyond `bash install.sh`.

### option B — CLI tool (requires Anthropic API key)

```bash
cp .env.example .env
# edit .env and add your ANTHROPIC_API_KEY
# get your key at console.anthropic.com (~$0.003 per roast)

python3 roast.py deck.pdf   # roast a PDF
python3 roast.py            # paste mode, press Enter twice to submit
```

---

## add your own funded decks (makes roasts sharper)

Drop PDF pitch decks into the `decks/` folder, then run:

```bash
python3 ingest.py
```

This extracts the text and adds it to `context/successful_decks.txt`.
Both `/roast` and the CLI automatically load this context.

The repo ships with 12 pre-ingested funded decks out of the box:

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

> The PDFs themselves are not in the repo (copyright). Only the extracted text context is committed.

---

## how it works

```
your deck (PDF or paste)
        ↓
   text extraction  ← PyMuPDF (text-based PDFs)
        ↓
   funded deck context  ← context/successful_decks.txt
        ↓
   brutal VC persona  ← Claude AI
        ↓
   roast + 3 actionable fixes
```

---

## project structure

```
roast-my-deck/
├── src/
│   ├── extractor.py      PDF text extraction (text-based + OCR fallback)
│   ├── ingestor.py       bulk deck ingestion
│   ├── roaster.py        Claude API calls (CLI mode)
│   └── formatter.py      terminal output formatting
├── skill/
│   └── SKILL.md          /roast skill for Claude Code
├── context/
│   └── successful_decks.txt   pre-ingested funded deck context ✓ committed
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

PRs welcome — especially:
- More funded deck PDFs (run `python3 ingest.py` and commit the updated `context/successful_decks.txt`)
- Better OCR support for image-based PDFs
- Additional roast personas (angels, accelerators, corporate VCs)

---

## stack

- Python 3.10+
- Claude claude-sonnet-4-20250514 — CLI mode
- Claude Code skill — `/roast` mode (no API key)
- PyMuPDF — PDF extraction
- Colorama — terminal colors

---

## license

MIT
