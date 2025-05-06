from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Predefined queries and their responses
QUERIES = {
    "What is the total revenue?": "The total revenue is $1,000,000",
    "How has net income changed over the last year?": "Net income has increased by 15% compared to last year",
    "What are the main expenses?": "The main expenses are: Salaries (40%), Operations (30%), and Marketing (20%)",
    "What is the profit margin?": "The current profit margin is 25%",
    "What is the cash flow situation?": "The company has a positive cash flow of $200,000"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def process_query():
    user_query = request.json.get('query', '').strip()
    
    # Find the best matching predefined query
    response = "I'm sorry, I don't understand that query. Please try one of the following:\n" + \
               "\n".join(f"- {query}" for query in QUERIES.keys())
    
    for predefined_query in QUERIES:
        if user_query.lower() in predefined_query.lower():
            response = QUERIES[predefined_query]
            break
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True) 