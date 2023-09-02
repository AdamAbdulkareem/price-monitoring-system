import json
from scraper import scraper
from scraper import soup, page
from scraper import check_product_title, check_product_id, check_price, check_date

            
# Function that save info of Amazon products to JSON file
def save_to_file():
    product_title = check_product_title(soup, page)
    product_id = check_product_id(soup)
    price = check_price(soup)
    date_info = check_date()
    product_data = {
        "ProductName": product_title,
        "ProductId": product_id,
        "Price": price,
        "Date_Time": date_info,
    }
    try:
        # Try to read the existing JSON data from the file
        with open("product_data.json", mode="r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist (first time), initialize an empty dictionary
        data = {}
        
    except json.JSONDecodeError:
        # If there's an error in decoding the JSON, handle it appropriately
        print("Error: Unable to decode the existing JSON data")
        return
    
    # Update the data with the new product_data
    data[product_id] = product_data

    try:
        # Write the updated data back to the file
        with open("product_data.json", mode="w", encoding="utf-8") as json_file:
            json.dump(data, json_file)
            
    except Exception as e:
        # Handle any unexpected errors during file writing
        print("Error: Unable to write to product_data.json:", e)


save_to_file()
