# Google Maps lead scraper

Playwright scraper that pulls business leads from Google Maps by keyword — name, rating, phone, website, email (regex-harvested from the site), and address — into CSV. Part of a cold-outreach lead pipeline.

```bash
pip install playwright pandas && playwright install chromium
python main.py "restaurant alger" my_run      # -> outputs/my_run/*.csv
./run_multiple_keywords.sh                     # batch several keywords
```

`extract_emails.py`, `merge.py` and `generate_messages.py` post-process the results; `visualizer/` is a small HTML view of a run.

> Scraped lead data (CSV/JSON outputs) is gitignored. Scrape only what you're allowed to, and respect each site's terms.
