# Usage example
from dashboard.helpers import ReceiptScraper, ReceiptProcessor


scraper = ReceiptScraper("files/1.jpg")
text = scraper.extract_receipt_text()

processor = ReceiptProcessor(text)
processor.process_receipt()