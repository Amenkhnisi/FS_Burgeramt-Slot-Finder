from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def scrape_appointments_playwright_sync():
    """
    Scrapes available Bürgeramt 'Anmeldung' appointments in Berlin.
    Uses Playwright sync API to avoid asyncio issues on Windows.
    """
    url = (
        "https://service.berlin.de/terminvereinbarung/termin/tag.php"
        "?termin=1"
        "&anliegen[]=120686"  # Anmeldung service code
        "&dienstleisterlist=122281,324414,122283,122279"  # example offices
        "&herkunft=1"
    )

    slots = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    for link in soup.select("a[aria-label]"):
        aria = link.get("aria-label", "")
        href = link.get("href", "")
        if "An diesem Tag einen Termin buchen" in aria and "termin/time" in href:
            try:
                date_str = aria.split(" - ")[0].strip()  # e.g., "15.10.2025"
                dt = datetime.strptime(date_str, "%d.%m.%Y").date()
                slots.append({
                    "date": dt.isoformat(),
                    "label": aria,
                    "link": f"https://service.berlin.de{href}"
                })
            except ValueError:
                continue

    return slots
