# Quotes Scraper — starter project

What
- A simple Python scraper that collects quotes, authors and tags from http://quotes.toscrape.com.

How to run (local)
1. Create and activate a virtualenv:
   python -m venv venv
   venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the scraper:
   python scraper.py --output quotes.csv

4. Run the demo analysis:
   python demo_analysis.py --input quotes.csv --outdir assets

Notes
- This project scrapes quotes.toscrape.com, a site made for practice. Always check robots.txt and site terms before scraping other sites.