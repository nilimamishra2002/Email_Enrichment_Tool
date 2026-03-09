# Email → Company & Sector Identification Tool

A lightweight **data enrichment tool** that identifies **company name and industry sector** from email addresses.

The system simulates **Google-like search behavior** using open-source web scraping tools without relying on paid APIs.

It processes both **single emails and bulk CSV files**, enriches them with company and sector information, and allows users to **export the results as an Excel file**.

---

## Project Overview

Organizations often need to enrich large lists of email addresses with additional information such as company and industry.

This tool automates that process by analyzing the **email domain**, searching the web for the related company, scraping the company website, and classifying the **industry sector** using keyword-based analysis.

The results are displayed through a simple **web interface** and can be downloaded as an **Excel report**.

---

## Key Features

- Extracts **domain and likely person name** from email
- Identifies **corporate vs personal email domains**
- Performs **web search simulation** using Selenium
- Scrapes company websites for contextual information
- Classifies the **industry sector** using keyword scoring
- Calculates **confidence levels** for predictions
- Supports **bulk processing via CSV upload**
- Allows **Excel download of enriched results**
- Simple and clean **Flask web interface**

---

## Technology Stack

**Backend**

- Python
- Flask

**Web Scraping**

- Selenium
- BeautifulSoup
- Requests
- WebDriver Manager

**Data Processing**

- Pandas
- Scikit-learn (optional experimentation)

**Frontend**

- HTML
- CSS

---

## Project Structure
Email_Enrichment_Tool
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── src
│   ├── parser.py
│   ├── domain.py
│   ├── scraper.py
│   ├── search.py
│   ├── classifier.py
│   └── confidence.py
│
├── templates
│   └── index.html
│
├── data
│   └── input.csv
│
└── test_selenium.py
---

## How the System Works

### 1. Email Parsing
The system extracts the **domain** and a probable **person name** from the email address.

Example:
hr@tcs.com

Output:

- Domain → `tcs.com`
- Name → `Hr`

---

### 2. Domain Classification

Domains are classified into two types:

| Type | Example |
|-----|------|
| Free Provider | gmail.com |
| Corporate Domain | tcs.com |

Free provider emails are marked as **personal emails**.

---

### 3. Company Identification

For corporate domains, the tool performs a search query:
domain + company
Example:
tcs.com company

Using **Selenium with DuckDuckGo**, the first search result title is extracted to determine the **company name**.

---

### 4. Website Scraping

The tool retrieves text from key pages of the company website:

- Homepage
- `/about`
- `/about-us`
- `/company`

Extracted elements include:

- Page title
- Meta description
- Headings
- Paragraph text

This information helps determine the company's industry sector.

---

### 5. Sector Classification

The collected text is analyzed using **keyword-based scoring** across industries such as:

- IT Services
- E-Commerce
- Financial Services
- Healthcare
- Manufacturing
- Energy
- Telecommunications
- Transportation
- Education

The sector with the highest keyword match score is selected.

---

### 6. Confidence Score

A confidence level is assigned based on:

- Domain type
- Keyword match strength
- Classification score

Possible outputs include:

- High Confidence
- Medium Confidence
- Low Confidence

---

## Example Output

| Email | Company | Sector | Confidence |
|------|------|------|------|
| hr@tcs.com | TCS | IT Services | Medium Confidence |
| support@flipkart.com | Flipkart | E-Commerce | Medium Confidence |
| contact@stripe.com | Stripe | Financial Services | High Confidence |
| user@gmail.com | Personal Email | N/A | Medium Confidence |

---

## Installation

Clone the repository:
git clone https://github.com/nilimamishra2002/Email_Enrichment_Tool.git

Navigate to the project folder:
cd Email_Enrichment_Tool
Install dependencies:
pip install -r requirements.txt
---

## Running the Application
Start the Flask server:
python app.py
Open your browser and visit:
http://127.0.0.1:5000

---

## Usage

### Single Email

Enter an email address in the input field and click **Enrich**.

---

### Bulk Processing

Upload a CSV file with the following format:
email
hr@tcs.com
contact@infosys.com
support@flipkart.com

---

### Export Results

After processing, users can download the enriched data as an **Excel file**.

---

## Limitations

- Sector detection depends on available website content
- Some websites block scraping requests
- Classification accuracy varies depending on text quality

---

## Possible Improvements

- Machine learning based sector classification
- Improved company identification
- Knowledge graph enrichment
- Asynchronous scraping for large datasets

---

## Author

**Nilima Mishra**
