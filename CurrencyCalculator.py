from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env


app = Flask(__name__)

# Setting Base URL and API KEY
BASE_URL = "https://v6.exchangerate-api.com/v6/"
API_KEY = os.getenv("API_KEY")


# Home Route where the URL will be 
@app.route('/', methods = ['GET', 'POST'])
def home():    
    return jsonify({"message" : "Hello This is Pra's Currency Converting API!"})
    

# Convert route where we can convert the amount from a currency to the desired currency
# It takes 3 values from the URL and uses them in the convert function
@app.route('/convert', methods = ['GET'])
def convert():

    # Gets the Dynamic data from by query method
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    amount = request.args.get('amount', type=float)

    if not from_currency or not to_currency or amount is None:
        return jsonify({"error" : "Missing required parameters: from, to, amount"}), 400
    

    if not API_KEY:
        return jsonify({"error" : "API Key is missing or not set"}), 500


    # Fetch conversion rate
    url = f"{BASE_URL}{API_KEY}/latest/{from_currency}"
    # creates a Response and JSONise it
    response = requests.get(url)


    if response.status_code != 200:
        return jsonify({"error" : "Failed to fetch exchange rate"}), response.status_code


    data = response.json()


    if to_currency not in data.get("conversion_rates", {}):
        return jsonify({"error": f'Invalid currency code: {to_currency}'}), 400
    

    # gets the currency rate of the currency to be converted
    to_currency_rate = data["conversion_rates"][to_currency]


    # Multiply the amount by the rate 
    result =  amount * to_currency_rate


    # Parses the result in a JSON format for further use
    return jsonify({
        'from': from_currency,
        'to': to_currency,
        'amount': amount,
        'converted_amount': result
    })



if __name__ == "__main__":
    app.run(debug = True)