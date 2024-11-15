
# OCR Receipt Scraping and Dashboard Project

This project utilizes Optical Character Recognition (OCR) to extract information from scanned receipts, processes the data using regular expressions (regex), and displays the results on a dashboard. The dashboard shows insights such as total sales, sales by payment type, and monthly sales trends.

## Features

- **OCR for Receipt Extraction**: Uses OCR to scan and extract data from receipt images.
- **Data Processing with Regex**: Regular expressions (regex) are used to identify and process key information like transaction dates, payment types, and amounts from the OCR text output.
- **Dashboard**: Visualizes extracted and processed data through various charts and tables, such as:
  - Total sales by payment type (Card, Cash, Other)
  - Monthly sales trends
  - Payment type percentages in a donut chart

## Technologies Used

- **OCR Library**: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for extracting text from images.
- **Python**: Primary language for the backend.
- **Django**: Web framework for backend development and rendering the dashboard.
- **JavaScript**: For dynamic interaction and chart rendering on the frontend.
- **Bootstrap**: For UI styling and layout.
- **Regex**: For text processing and extracting relevant data from OCR results.
- **Chart.js**: For visualizing data on the dashboard (e.g., bar and donut charts).

## Setup Instructions

### Prerequisites

Ensure you have the following installed:
- Python (>= 3.7)
- Django (>= 3.0)
- **Tesseract OCR** (see instructions below for installation)
- Node.js (for frontend charting if needed)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/receipt-dashboard.git
cd receipt-dashboard
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

Tesseract OCR is used to extract text from scanned receipt images. Follow the instructions below to install it on your system.

#### For Windows

1. **Download the Tesseract installer** from the official Tesseract at UB Mannheim repository:
   - Go to the [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) page.
   - Download the **latest Windows installer** (exe file).
   
2. **Run the installer**:
   - Follow the installation prompts, keeping the default settings.
   - During installation, make sure to select the option to add Tesseract to the system path (this will allow you to use Tesseract from the command line).
   
3. **Verify Installation**:
   - Open the Command Prompt (CMD) and type:
     ```bash
     tesseract --version
     ```
   - You should see the installed version of Tesseract, confirming it’s correctly installed.

4. **Download Additional Language Files (Optional)**:
   - You can download additional language files if needed. This can be done during installation or by visiting the Tesseract language files repository.

#### For macOS

1. **Install Tesseract via Homebrew**:
   - If you don't have Homebrew installed, you can install it by running:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   
2. **Install Tesseract**:
   - Once Homebrew is installed, you can install Tesseract by running:
     ```bash
     brew install tesseract
     ```

3. **Verify Installation**:
   - Open the terminal and type:
     ```bash
     tesseract --version
     ```
   - You should see the installed version of Tesseract, confirming it’s correctly installed.

4. **Download Additional Language Files (Optional)**:
   - If you need additional language files for OCR, install them using the following command:
     ```bash
     brew install tesseract-lang
     ```

### 4. Set Up the Database

```bash
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser to view the dashboard.

## Project Structure

```bash
receipt-dashboard/
│
├── dashboard/
│   ├── migrations/
│   ├── models.py               # Models for receipts and items
│   ├── views.py                # Views for handling dashboard and data
│   ├── helpers.py              # Functions for data processing (OCR, regex, sales calculations)
│   ├── templates/
│   │   ├── dashboard/
│   │   │   ├── index.html      # Dashboard HTML with chart rendering
│   ├── static/
│       ├── js/
│       │   └── chart.js        # JavaScript for rendering charts
├── manage.py                   # Django management script
├── requirements.txt            # Project dependencies
└── README.md                   # This file
```

## Data Flow

1. **OCR Extraction**: Receipts are uploaded as image files, and OCR (via Tesseract) extracts the text from the image.
2. **Regex Processing**: The extracted text is processed using regular expressions to capture relevant data, such as:
   - Transaction date (to calculate monthly sales trends)
   - Payment type (to calculate payment type distribution)
   - Total amount (for calculating total sales)

### Dashboard Display

The dashboard is built using Django's templating system and renders dynamic charts using Chart.js. The following key features are visualized:
- **Sales by Payment Type**: A donut chart showing the percentage of total sales for each payment type.
- **Monthly Sales Trends**: A bar chart displaying sales totals by month for the current year.
- **Total Sales**: Displays the total sales for each payment type (Card, Cash, Other).

## Contribution

Contributions are welcome! If you would like to improve the project, feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License.

