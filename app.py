from flask import Flask, render_template, request
import csv
import requests
import os

app = Flask(__name__)

CSV_FILE = 'results.csv'

# Function to fetch official CSV (only if server online)
def fetch_official_csv():
    url = 'https://example.com/official_results.csv'  # replace with real URL if legal
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(CSV_FILE, 'wb') as f:
                f.write(response.content)
            print("Official CSV fetched & saved locally ✅")
        else:
            print("Server unreachable or CSV not ready ❌")
    except Exception as e:
        print("Error fetching CSV:", e)

# Function to read CSV
def get_result(register_number):
    results = []
    if not os.path.exists(CSV_FILE):
        return None
    with open(CSV_FILE, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['RegisterNumber'] == register_number:
                results.append(row)
    return results

@app.route('/')
def index():
    # Try fetch official CSV (first time only)
    fetch_official_csv()
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    regno = request.form['regno']
    data = get_result(regno)
    return render_template('result.html', regno=regno, data=data)

if __name__ == '__main__':
    app.run(debug=True)

