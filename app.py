from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime


app = Flask(__name__)

#Predefined Queries
TeslaSummary = '''
Tesla
Revenue Growth

2023: +18.80%
2024: +0.95%
Net Income Growth

2023: +18.96%
2024: -52.23%
Observations: 

Tesla had a sharp revenue surge in 2023, followed by stagnation in 2024.
The massive drop in net income in 2024 is a red flag.
Operating cash flow remained flat (approximately 14.9 billion).
Total Assets grew significantly from 82.3 billion to 122.1 billion.
Average Revenue over 3 years: 91.9 billion.

'''
QUERIES = {
    "What is the total revenue of Apple in year 2023?":"The total revenue of apple in year 2023 is $211,915M.",
    "How has the net income of Microsoft changed over the last year?":"The net income of Microsoft has increased by 15.67%",
    "What would be the financial summary of Tesla over the past 3 years?":TeslaSummary,
    "What is the cash flow situation of Tesla?":"Tesla consistently posts the lowest cash flow margins among the three, declining from around 18% in 2022 to approximately 15% in 2024. This suggests potential constraints in converting revenue into operating cash flow.",
    "What is the Debt to Asset ratio analysis of Apple?":"Apple's debt-to-asset ratio has remained relatively stable, with a slight increase from 32.6% in 2023 to 33.4% in 2024. This suggests a modest rise in liabilities relative to total assets."
}

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/query', methods = ['POST'])
def process_query():
    user_query = request.json.get('query','').strip()

    response = "I'm sorry, I don't understand that query. Please try one the following: \n" + \
                    "\n".join(f"- {query}" for query in QUERIES.keys())
    
    for predefined_query in QUERIES:
        if user_query.lower() in predefined_query.lower():
            response = QUERIES[predefined_query]

    return jsonify({'response':response})

if __name__ == '__main__':
    app.run(debug = True)