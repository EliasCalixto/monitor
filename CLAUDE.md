# CLAUDE.md

# comment

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Local CLI (matplotlib):**
```bash
python monitor.py              # current month
python monitor.py jan26        # single month by alias
python monitor.py jan25 dec25  # range by alias
python monitor.py 28 39        # range by row index
```

**Fetch Notion data locally:**
```bash
NOTION_TOKEN=secret_xxx NOTION_PAGE_ID=<32-char-hex> python scripts/fetch_notion.py
```

**Serve dashboard locally:**
```bash
python -m http.server -d docs 8000
# then open http://localhost:8000
```

## Architecture

Two independent tools sharing no runtime code:

### 1. CLI visualizer (`monitor.py`, `setup.py`, `arguments_helper.py`)

- `setup.py` reads `~/Library/CloudStorage/OneDrive-Personal/Shared/Main.xlsx` (sheet `DataRaw`) into a global `df`. Row index = month (0 = Sep 2022). `current_row` is computed by counting rows with any non-zero category sum.
- `arguments_helper.py` maps month aliases (`jan26`, `feb26`, …) → row indices. Used by `monitor.py` to translate CLI args before calling `get_totals(start, end)`.
- `monitor.py` renders a 3-panel matplotlib figure: bar chart (top-left), donut (top-right), and a category-by-month bar chart with a slider (bottom, full-width).

### 2. Notion → GitHub Pages dashboard (`scripts/fetch_notion.py`, `docs/`)

**Data flow:**
1. `fetch_notion.py` walks child databases under the Notion Monitor page and serializes them into `docs/data.json`.
2. GitHub Actions (`.github/workflows/sync-notion.yml`) runs every 15 minutes, commits `data.json` to `main`, which GitHub Pages serves.
3. `docs/dashboard.js` fetches `data.json` on load, parses it, and renders charts using Chart.js 4.

**`data.json` shape:**
```json
{
  "generated_at": "<ISO timestamp>",
  "databases": [
    {
      "id": "...",
      "title": "...",
      "schema": { "<column>": "<notion-type>", ... },
      "rows": [ { "_id": "...", "_url": "...", "<prop>": <value>, ... } ]
    }
  ]
}
```
If `DATA_PASSPHRASE` is set as a GitHub secret, `data.json` is instead an AES-256-GCM envelope (`v`, `kdf`, `iters`, `salt`, `iv`, `ct` fields). The browser decrypts it via WebCrypto; passphrase is cached in `localStorage`.

**Dashboard JS (`docs/dashboard.js`):**
- Single-file vanilla JS with no build step. State lives in the `state` object.
- Two Notion databases are expected: **Expenses** and **Incomes**. The dashboard auto-detects which database is which by presence of category columns.
- Filtering is by `period` (preset date ranges) and `selectedCategories` (Set of category names). All chart/table renders read these from `state` and re-render fully.
- Charts use Chart.js with the `chartjs-plugin-datalabels` plugin for value labels.

## Fixed categories and color palette

Both the CLI and the dashboard share the same 8 categories and colors (must stay in sync):

| Category | Hex       |
|----------|-----------|
| Savings  | `#8dbad6` |
| Setup    | `#9bc2e7` |
| Home     | `#8ea9db` |
| Studies  | `#abb9d4` |
| Enjoy    | `#b9f5c4` |
| Losses   | `#fd9a9a` |
| Fixed    | `#f8ccad` |
| Cashout  | `#fef2cb` |

The CLI darkens these colors by 20% (`darken()` in `monitor.py`) when used in the line chart, but not in bar/donut charts.

## GitHub Actions

The workflow (`sync-notion.yml`) triggers on schedule (`*/15 * * * *`), `workflow_dispatch`, and pushes to `scripts/fetch_notion.py` or the workflow file itself. It uses `pycryptodome==3.20.0` for optional encryption. Required secrets: `NOTION_TOKEN`, `NOTION_PAGE_ID`; optional: `DATA_PASSPHRASE`.
