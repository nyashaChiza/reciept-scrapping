# Usage example
from src.scrap import ReceiptScraper


scraper = ReceiptScraper("files/1.jpg")
text = scraper.extract_receipt_text()
print(text)