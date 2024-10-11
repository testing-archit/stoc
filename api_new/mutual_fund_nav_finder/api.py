from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Fetch NAV data from the AMFI India website
def fetch_nav_data():
    url = "https://www.amfiindia.com/spages/NAVAll.txt"
    try:
        response = requests.get(url, timeout=10)  # 10-second timeout
        response.raise_for_status()  # Raise an error for bad responses (4XX, 5XX)
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching NAV data: {e}")
        return None

# Parse the NAV data into a dictionary
def parse_nav_data(data):
    nav_dict = {}
    lines = data.splitlines()
    for line in lines[1:]:  # Skip header line
        parts = line.split(';')  # Based on semicolon delimited data
        if len(parts) > 4:  # Ensure that there are enough columns
            fund_name = parts[3].strip()  # Mutual fund name
            nav_value = parts[4].strip()  # NAV value
            nav_dict[fund_name] = nav_value
    return nav_dict

# Main route to handle GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def home():
    nav_value = None
    if request.method == 'POST':
        fund_name = request.form['fund_name']
        data = fetch_nav_data()

        if data:
            nav_data = parse_nav_data(data)
            nav_value = nav_data.get(fund_name, "Fund not found")  # Default message if not found
        else:
            nav_value = "Error fetching NAV data."

    return render_template('index.html', nav_value=nav_value)

# Run the app on port 5001
if __name__ == '__main__':
    app.run(debug=True, port=5010)

