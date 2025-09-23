import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.services.scraper import scrape_appointments_playwright_sync


@pytest.fixture
def mock_html():
    return """
    <html>
        <body>
            <a aria-label="15.10.2025 - An diesem Tag einen Termin buchen"
               href="/termin/time/12345">Book</a>
            <a aria-label="Invalid date - An diesem Tag einen Termin buchen"
               href="/termin/time/67890">Book</a>
            <a aria-label="15.10.2025 - Not a booking link"
               href="/other/path">Ignore</a>
        </body>
    </html>
    """


def test_scrape_appointments_playwright_sync(mock_html):
    mock_browser = MagicMock()
    mock_page = MagicMock()
    mock_page.content.return_value = mock_html
    mock_browser.new_page.return_value = mock_page

    mock_playwright = MagicMock()
    mock_playwright.chromium.launch.return_value = mock_browser

    def mock_get_valid(key, default=None):
        return {
            "aria-label": "15.10.2025 - An diesem Tag einen Termin buchen",
            "href": "/termin/time/12345"
        }.get(key, default)

    mock_link = MagicMock()
    mock_link.get.side_effect = mock_get_valid

    with patch("app.services.scraper.sync_playwright") as mock_sync_playwright, \
            patch("app.services.scraper.BeautifulSoup") as mock_bs:

        mock_sync_playwright.return_value.__enter__.return_value = mock_playwright
        mock_bs.return_value.select.return_value = [mock_link]

        slots = scrape_appointments_playwright_sync()

        assert len(slots) == 1
        assert slots[0]["date"] == "2025-10-15"
