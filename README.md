# StarCitizen Trade Planner

*Deutsche Fassung: [README.de.md](README.de.md)*

A standalone HTML tool (works offline) for commodity trading in Star Citizen: **top trade routes**, a **trade overview of every commodity** with all buy and sell locations, views **by sell and buy location** and a **cargo calculator** – same layout and handling as the [Blueprint Planner](https://github.com/Jaegerfeld/StarCitizen-Bauplan-Planer) and [Wikelo Planner](https://github.com/Jaegerfeld/StarCitizen-Wikelo-Planer).

**🌐 Online version:** https://jaegerfeld.github.io/StarCitizen-Handels-Planer/

## Features

- **Routes:** three tables – legal bulk routes (buy stock ≥ 100 SCU), highest margins overall, illegal routes – with buy/sell place, prices, margin per SCU and, for the chosen cargo size, **outlay and profit per load**. Warns when the stock at the buy place is smaller than your cargo.
- **All commodities:** every commodity with best buy place (cheapest with stock), best sell place, margin, stock; search, filters (type, legality, system), sortable columns; click a row to see **all** buy and sell places with price, stock, container sizes and date.
- **By sell location / by buy location:** per place, what sells there at a profit or what loads there with a good margin (plan multi-commodity cargo).
- **Cargo calculator:** Cutlass Black (46), Freelancer (66), Mercury Star Runner (114) or a custom SCU value.
- Bilingual (DE/EN), light/dark, choices persisted in the browser.
- **Daily data:** the online version is rebuilt every day (GitHub Actions, 05:00 UTC). The button "Load latest build (GitHub)" fetches that build's `data.json` from GitHub Pages – also from an offline copy – instead of hitting star-head directly. Right-click resets to the built-in data.
- **Downloads** (online version): `SC_Waren_Handelsuebersicht.xlsx`, `SC_Waren_Top_Handelsrouten.md`, `data.json`.

## Usage

- **Just use it:** open the online version above, or double-click `SC_Handels_Planer.html` (works fully offline).
- **Rebuild with fresh data:** run `Handels_Planer_aktualisieren.bat` (Windows) / `.sh` (Linux) / `.command` (macOS), or:

  ```bash
  python handels_planer_bauen.py          # HTML + data.json + routes Markdown
  python handels_planer_bauen.py --xlsx   # plus the Excel file (needs openpyxl)
  python handels_planer_bauen.py --cache  # raw data from handel_cache.json (for development, spares star-head)
  ```

  This pulls commodities, shops and prices from star-head.de (about 280 requests, 10–30 s) and bakes them into `SC_Handels_Planer.html`. Only the Python standard library is required; `openpyxl` only for `--xlsx`.

## Own data from terminal screenshots

Prices you read off a trade terminal yourself come in through the [SC Screenshot Evaluator](https://github.com/Jaegerfeld/StarCitizen-Screenshot-Auswerter): put its reviewed `auswertung.json` into the folder `eigene_daten/` and rebuild. Same shop + commodity + side replaces the star-head row, new ones are added, rows still marked "to check" stay out. Such rows are tagged "own data" in the commodity detail table. Alternatively `python handels_planer_bauen.py --eigene <file|folder>`. The folder stays local (gitignored); the online version holds star-head data only.

## How it works

- `handel_core.py` – the **single** place holding the business logic: fetching (`fetch_all`), best buy (cheapest place with stock > 0, else cheapest) and best sell (highest-paying place), margin, route selection (`select_routes`), per-location views, routes guide as Markdown.
- `handel_xlsx.py` – the Excel workbook from the same data.
- `handels_planer_bauen.py` – builds the app; every evaluation comes from `handel_core`, the app only renders.
- Data is **community-maintained** (star-head.de) and may be days old ("as of" per price row). Margin/SCU excludes fuel, time and risk. Verify in game before buying.

## Sources

- Commodities, shops, prices: **star-head.de** (API `commodity`, `shop`, `shopitem/price`, `celestialobject`, `location`)

## License

BSD-3-Clause, see `LICENSE`. Unofficial fan project, not affiliated with Cloud Imperium Games. Star Citizen® is a trademark of CIG.
