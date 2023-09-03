import asyncio
from flask import Flask, request, jsonify
from .scraper import main # Import the main function from scraper.py

app = Flask(__name__)

@app.route("/scrape_amazon", methods=["POST"])
def scrape_amazon():
    data = request.get_json()
    amazon_website = data.get("amazon_website")
    product_name = data.get("product_name")
    # Call the main function from scraper.py
    asyncio.run(main(amazon_website, product_name))
    
if "__name__" == "__main__":
    app.run(debug=True)