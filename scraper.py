# Import necessary libraries
from bs4 import BeautifulSoup
import requests
from datetime import date
from datetime import datetime

# Define the URL of the Amazon product page you want to scrape

URL = "https://www.amazon.com/dp/B09MSRJ97Y"
# URL = "https://www.amazon.com/dp/B09XBS3S5J"
# URL = "https://www.amazon.com/dp/B0BDTWQ2DW"
# URL = "https://www.amazon.com/dp/B0863TXGM3"
#URL = "https://www.amazon.com/dp/B099VMT8VZ"

# Define headers to mimic a web browser's request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Upgrade-Insecure-Requests": "1",
}
try:
    # Send an HTTP GET request to the specified URL with the headers
    page = requests.get(URL, headers=headers)
    
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    
    # Define a function to check and extract the product title
    def check_product_title():
        """
        Extracts and returns the product title from the Amazon product page.

        Returns:
            str: The product title.
        """
        product_title =  soup.find("span", id="productTitle").text.strip()
        print(f"Product Title:{str(product_title)}")
        return product_title

    # Define a function to check and extract the product ID
    def check_product_id():
        """
        Extracts and returns the product ID from the Amazon product page.

        Returns:
            str: The product ID.
        """
        product_id_element = soup.find(
            "div", id="title_feature_div", attrs={"data-csa-c-asin": True}
        )
        return product_id_element["data-csa-c-asin"]
    
    # Define a function to check and extract the product price
    def check_price():
        """
        Extracts and returns the product price from the Amazon product page.

        Returns:
            float: The product price as a floating-point number.
        """
        price_string = soup.find("span", class_="a-offscreen").text.strip("$")
        return float(price_string.replace(",", ""))
    
    # Define a function to check and extract product keywords
    def check_keywords():
        """
        Extracts and returns the product keywords or features from the Amazon product page.

        Returns:
            str: The product keywords or features.
        """
        return soup.find("div", id="featurebullets_feature_div").text.strip()
    
    # Define a function to get the current date and time
    def check_date():
        """
        Gets the current date and time.

        Returns:
            tuple: A tuple containing the current date and time in string format.
                (date, time)
        """
        current_date = date.today().strftime("%a, %B %d %Y")
        current_time = datetime.now().strftime("%H:%M:%S %p")
        return current_date, current_time

except requests.exceptions.RequestException as e:
    # Handle exceptions related to making the HTTP request
    print("Error in the request:", e)

except AttributeError as e:
    # Handle exceptions related to parsing the HTML content
    print("Error in parsing HTML:", e)

except Exception as e:
    # Handle unexpected exceptions
    print("An unexpected error occurred:", e)
