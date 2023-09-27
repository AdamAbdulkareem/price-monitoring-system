# Import necessary libraries
from bs4 import BeautifulSoup
import json
import requests
import asyncio
from datetime import date, datetime
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from urllib.parse import urlparse

# Define headers to mimic a web browser's request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Upgrade-Insecure-Requests": "1",
}

# Define a function to check and extract the product title
def check_product_title(soup, page):
    if page.status_code == 200:
        return soup.find("span", id="productTitle").text.strip()
    else:
        print("Failed to retrieve the page. Status code:", page.status_code)

# Define a function to check and extract the product ID
def check_product_id(soup):
    product_id_element = soup.find(
        "div", id="title_feature_div", attrs={"data-csa-c-asin": True}
    )
    return product_id_element["data-csa-c-asin"]

# Define a function to check and extract the product price
def check_price(soup):
    price_string = soup.find("span", class_="a-offscreen").text.strip("$")
    return float(price_string.replace(",", ""))

# Define a function to check and extract product keywords
def check_keywords(soup):
    return soup.find("div", id="featurebullets_feature_div").text.strip()

# Define a function to get the current date and time
def check_date():
    current_date = date.today().strftime("%a, %B %d %Y")
    current_time = datetime.now().strftime("%H:%M:%S %p")
    return current_date, current_time

async def main(url, search_text):
    global soup, page 
    urls_metadata = {
    url: {
        "search_field_query": 'input[name="field-keywords"]',
        "search_button_query": 'input[value="Go"]',
        "product_selector": "div.s-card-container"
    }
}
    
    metadata = urls_metadata.get(url)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await stealth_async(page)
        await page.goto(url, timeout=300000)
        search_page = await search(metadata, page, search_text)
        # await search_page.screenshot(path="amazon-product.png")
        return await get_products(page)
    
        # max_retries = 5
        # retry_count = 0

        # while retry_count < max_retries:
        #     try:
        #         # Send an HTTP GET request to the specified URL with the headers
        #         page = requests.get(product_page_url, headers=headers)
                
        #         # Parse the HTML content of the page using BeautifulSoup
        #         soup = BeautifulSoup(page.content, "html.parser")
            
        #         product_title = check_product_title(soup, page)
        #         product_id = check_product_id(soup)
        #         price = check_price(soup)
        #         date_info = check_date()

        #         # Check if product_id and product_title are not None or empty
        #         if product_title is not None and product_id:
        #             break  # Break out of the loop if both values are valid

        #         # If either product_id or product_title is None or empty, retry
        #         retry_count += 1
        #     except Exception as e:
        #         print(f"An error occurred: {str(e)}")
        #         retry_count += 1

        # if retry_count >= max_retries:
        #     print("Max retries reached. Unable to fetch valid product information.")

        # This function save the product info to a json file
        # def save_to_file():
        #     product_data = {
        #         "ProductName": product_title,
        #         "ProductId": product_id,
        #         "Price": price,
        #         "Date_Time": date_info,
        #     }
            
        #     try:
        #         # Try to read the existing JSON data from the file
        #         with open("product_data.json", mode="r", encoding="utf-8") as json_file:
        #             data = json.load(json_file)
        #     except FileNotFoundError:
        #         # If the file doesn't exist (first time), initialize an empty dictionary
        #         data = {}
        
        #     except json.JSONDecodeError:
        #         # If there's an error in decoding the JSON, handle it appropriately
        #         print("Error: Unable to decode the existing JSON data")
        #         return
    
        #     # Update the data with the new product_data
        #     data[product_id] = product_data

        #     try:
        #         # Write the updated data back to the file
        #         with open("product_data.json", mode="w", encoding="utf-8") as json_file:
        #             json.dump(data, json_file)
            
        #     except Exception as e:
        #         # Handle any unexpected errors during file writing
        #         print("Error: Unable to write to product_data.json:", e)
                
        # save_to_file()

async def search(metadata, page, search_text):
    search_field_query = metadata.get("search_field_query")
    search_button_query = metadata.get("search_button_query")

    search_box = await page.wait_for_selector(search_field_query)
    await search_box.type(search_text)
    button = await page.wait_for_selector(search_button_query)
    await button.click()
    await page.wait_for_load_state('load')
    return page

async def get_products(page):
    arr_products = []
    product_selector = 'div[data-asin][data-component-type="s-search-result"]'
    product_divs = await page.query_selector_all(product_selector)

    for product in product_divs:
        span_tag = await product.query_selector('span.a-size-medium.a-color-base.a-text-normal')
        span_text = await span_tag.inner_text()
        data_asin = await product.get_attribute('data-asin')
        img_selector = await product.query_selector('img.s-image')
        img_src = await img_selector.get_attribute('src')
        product_info = {
            "product_title" : span_text,
            "product_id" : data_asin,
            "product_img_url" : img_src
        }
        arr_products.append(product_info)
        # await select_product(page, product)
    return arr_products

# async def select_product(category_page, product):
#     link_tag = await product.query_selector('a.a-link-normal')
#     await link_tag.click()
#     await category_page.wait_for_load_state('load')
#     await category_page.screenshot(path="amazon-product_1.png")
#     # Parse the URL
#     parsed_url = urlparse(category_page.url)

#     # Extract the useful part (without query parameters)
#     useful_part = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
#     global product_page_url
#     product_page_url = useful_part


#asyncio.run(main("https://www.amazon.com", "CPU Gaming Processor"))