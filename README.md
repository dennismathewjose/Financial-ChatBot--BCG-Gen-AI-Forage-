# Financial-ChatBot – BCG GenAI Forage

## Overview

The GenAI Consulting team at BCG has partnered with Global Finance Corp. (GFC), a leading global financial institution, to develop an AI-powered chatbot that transforms how corporate financial performance is analyzed and consumed.

In an era of growing data volumes and rapidly changing markets, GFC seeks to modernize its financial analysis process by replacing traditional, time-intensive workflows with a scalable, intelligent, and interactive solution powered by Generative AI and Natural Language Processing (NLP).

---

## Project Objective

The primary goal is to build a conversational AI tool that:

- Analyzes and interprets financial data from 10-K and 10-Q filings
- Provides summarized insights into corporate financial health
- Offers a natural, intuitive interface for GFC’s clients—regardless of financial expertise

This tool is expected to enhance decision-making, boost productivity, and accelerate financial analysis.

---

## Chatbot Features

- Web-based interface with real-time chat functionality
- Clean, modern, and responsive design (works on both desktop and mobile)
- Predefined queries and financial responses
- Simple and intuitive user experience

---

## Predefined Queries (Sample)

1. What is the total revenue of Apple in year 2023?
2. How has the net income of Microsoft changed over the last year?
3. What would be the financial summary of Tesla over the past 3 years?
4. What is the cash flow situation of Tesla?
5. What is the Debt to Asset ratio analysis of Apple?

---

## Data Extraction

The chatbot relies on manually curated data extracted from SEC EDGAR 10-K filings for Apple, Tesla, and Microsoft over the past three fiscal years.

Key financial metrics collected:

- Total Revenue
- Net Income
- Total Assets
- Total Liabilities
- Cash Flow from Operating Activities

---

## Data Analysis

Performed year-over-year trend analysis and financial health evaluation using:

- Revenue and Net Income Growth (%)
- Debt-to-Asset Ratio
- Cash Flow Margin
- Net Profit Margin

The data was then structured for use within the chatbot's response logic.

---

## Data Preparation

- Cleaned and formatted data for integration
- Ensured consistency in naming, units, and structure
- Prepared the dataset for chatbot consumption

---

## Technologies Used

- Python (Pandas, NumPy, Matplotlib, Seaborn)
- Flask (Backend for chatbot interface)
- HTML/CSS/JavaScript (Web frontend)

---

## Setup Instructions

1. **Create and activate virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Install the dependencies:
``` bash   
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```
4. Access the chatbot:
```bash
Open a browser and navigate to http://localhost:5000
```
## Current Limitations
- Chatbot only supports a fixed set of predefined queries
- Responses are static (not connected to live financial data)
- Lacks dynamic natural language understanding
- Limited scope of financial metrics and no user personalization

## Upcoming Improvements
- Integration with real-time financial APIs or document parsers
- Implementation of NLP to support open-ended queries
- Expansion to support broader financial KPIs and company coverage
- Visual responses (e.g., charts and graphs)
- User authentication and personalized financial dashboards

## Authors
BCG GenAI Consulting Team – Forage Virtual Internship
- [Dennis Mathew Jose](https://www.linkedin.com/in/dennismjose/)

## License
This project is developed as part of an academic and exploratory initiative. No commercial license is attached.

