# roast-my-deck 🔥

A CLI tool that brutally roasts your pitch deck using Claude AI.
Train it on real funded decks and it gets even sharper.

Also ships as a `/roast` skill for Claude Code — no API key needed.

Built in one night. Open source. Free.

---

## install

```bash
git clone https://github.com/yourusername/roast-my-deck
cd roast-my-deck
bash install.sh
```

`install.sh` does three things:
1. Installs Python dependencies
2. Creates `.env` from `.env.example`
3. Installs the `/roast` skill for Claude Code (if detected)

---

## usage

### option A — Claude Code skill (no API key)

Open any Claude Code session in this directory:

```bash
/roast deck.pdf       # roast a PDF
/roast                # paste your deck content manually
```

Claude itself does the roasting. No API key, no cost.

### option B — CLI tool (requires API key)

Add your Anthropic API key to `.env`, then:

```bash
python3 roast.py deck.pdf   # roast a PDF
python3 roast.py            # paste mode, end with empty line
```

Get your key at [console.anthropic.com](https://console.anthropic.com). One roast costs ~$0.003.

### train on funded decks

Drop real pitch deck PDFs into the `decks/` folder, then:

```bash
python3 ingest.py
```

This extracts text from all decks and saves it to `context/successful_decks.txt`.
Both the CLI tool and the `/roast` skill will automatically load this context.

The more funded decks you add, the sharper the roasts.

---

## how it works

```
your deck (PDF or paste)
        ↓
   text extraction  (PyMuPDF)
        ↓
   funded deck context  (optional, from decks/ folder)
        ↓
   brutal VC persona  (Claude AI)
        ↓
   roast + 3 fixes
```

---

## project structure

```
roast-my-deck/
├── src/
│   ├── extractor.py    — PDF text extraction via PyMuPDF
│   ├── ingestor.py     — bulk funded deck ingestion
│   ├── roaster.py      — Claude API calls (CLI mode)
│   └── formatter.py    — terminal colors via colorama
├── skill/
│   └── SKILL.md        — /roast skill for Claude Code
├── decks/              — drop funded PDFs here (gitignored)
├── context/            — generated context lives here (gitignored)
├── tests/
│   └── test_roaster.py
├── roast.py            — CLI entry point
├── ingest.py           — ingestion entry point
└── install.sh          — one-command setup
```

---

## running tests

```bash
python3 -m pytest tests/ -v
```

---

## stack

- Python 3.10+
- Claude claude-sonnet-4-20250514 (Anthropic) — CLI mode
- Claude Code skill — `/roast` mode (no API key)
- PyMuPDF — PDF extraction
- Colorama — terminal colors

---

## contributing

PRs welcome. Especially more funded deck examples in `decks/`.

---

## license

MIT
