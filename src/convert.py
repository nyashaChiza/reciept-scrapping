import pytesseract
from PIL import Image
import pillow_heif
import os
import re  # Ensure 're' is imported for regular expressions

class HeicReceiptScraper:
    def __init__(self, directory):
        self.directory = directory

    def extract_text(self, image_path):
        try:
            # Open HEIC image using Pillow and pillow-heif (no need to use pillow_heif.open)
            image = Image.open(image_path)

            # Use pytesseract to extract text from the image
            text = pytesseract.image_to_string(image)

            return text
        except Exception as e:
            print(f"Error extracting text from {image_path}: {e}")
            return None

    def extract_receipt_details(self):
        # Iterate through all files in the directory
        for filename in os.listdir(self.directory):
            if filename.lower().endswith('.heic'):  # Only process .heic files
                heic_path = os.path.join(self.directory, filename)
                print(filename)

                # Extract text from the HEIC image
                text = self.extract_text(heic_path)

                if text:
                    print(f"Extracted text from {filename}:")
                    print(text)  # Print the extracted text (You can also save it to a file)

                    # Here you can add additional logic to scrape specific details like 'Total', 'Date', etc.
                    details = self.parse_receipt_details(text)
                    if details:
                        print(f"Receipt details for {filename}:")
                        print(details)

    def parse_receipt_details(self, text):
        # Example regex to find total amount, date, and store name (customize as per your receipt format)
        details = {}

        # Extract store name (this regex is just an example and might need modification based on receipt format)
        store_name = re.search(r"(Store|Merchant):\s*(.*)", text)
        if store_name:
            details['store'] = store_name.group(2)

        # Extract total amount (assuming format: Total: $xx.xx)
        total_amount = re.search(r"Total:\s*\$([0-9]+\.[0-9]{2})", text)
        if total_amount:
            details['total'] = total_amount.group(1)

        # Extract date (assuming format: Date: YYYY-MM-DD)
        date = re.search(r"Date:\s*(\d{4}-\d{2}-\d{2})", text)
        if date:
            details['date'] = date.group(1)

        return details


