import re
from datetime import datetime

class ReceiptProcessor:
    def __init__(self, receipt_text):
        self.receipt_text = receipt_text
        self.receipt_data = {}

    def clean_text(self):
        """Clean up unwanted characters, like extra spaces, line breaks, etc."""
        cleaned_text = re.sub(r'[-—\n]', ' ', self.receipt_text)  # Replace dashes and newlines with spaces
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Remove extra spaces
        self.receipt_text = cleaned_text

    def extract_data(self):
        """Extract key data from the receipt text."""
        # Extract date and time (transaction time) and remove AM/PM if in 24-hour format
        date_time_pattern = r'(\d{1,2} \w{3}\'\d{2} \d{1,2}:\d{2})'
        date_time_match = re.search(date_time_pattern, self.receipt_text)
        if date_time_match:
            self.receipt_data['date_time'] = date_time_match.group(0)

        # Extract receipt close time (for validation) and remove AM/PM if in 24-hour format
        close_time_pattern = r'(\d{1,2} \w{3}\'\d{2} \d{1,2}:\d{2})'
        close_time_matches = re.findall(close_time_pattern, self.receipt_text)
        if len(close_time_matches) > 1:
            self.receipt_data['close_time'] = close_time_matches[1]

    def validate_times(self):
        """Validate that the transaction time and close time are reasonable."""
        try:
            # Remove AM/PM and parse both times as 24-hour format
            transaction_time_str = self.receipt_data['date_time']
            close_time_str = self.receipt_data['close_time']
            transaction_time = datetime.strptime(transaction_time_str, "%d %b'%y %H:%M")
            close_time = datetime.strptime(close_time_str, "%d %b'%y %H:%M")

            # Calculate the time difference
            time_diff = close_time - transaction_time
            if time_diff.seconds > 300:  # 5 minutes threshold
                raise ValueError(f"Time difference between transaction and close time is too long: {time_diff}")
            print(f"Time difference: {time_diff}")
        except Exception as e:
            print(f"Error in validating times: {e}")
            raise

    def process_receipt(self):
        """Process the receipt: clean text, extract data, and validate."""
        self.clean_text()
        self.extract_data()
        self.validate_times()  # Ensure time consistency



