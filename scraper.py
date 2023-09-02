# Import necessary libraries
from bs4 import BeautifulSoup
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

amazon_website = "https://www.amazon.com"
urls_metadata = {
    amazon_website: {
        "search_field_query": 'input[name="field-keywords"]',
        "search_button_query": 'input[value="Go"]',
        "product_selector": "div.s-card-container"
    }
}

# Define a function to check and extract the product title
def check_product_title(soup, page):
    if page.status_code == 200:
        product_title =  soup.find("span", id="productTitle").text.strip()
        return product_title
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
    metadata = urls_metadata.get(url)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await stealth_async(page)
        await page.goto(url, timeout=120000)
        search_page = await search(metadata, page, search_text)
        await search_page.screenshot(path="amazon-product.png")
        await get_products(page)

        try:
            # Send an HTTP GET request to the specified URL with the headers
            page = requests.get(product_page_url, headers=headers)

            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(page.content, "html.parser")

            check_product_title(soup, page)
            check_product_id(soup)
            check_price(soup)
            check_keywords(soup)

        except requests.exceptions.RequestException as e:
            # Handle exceptions related to making the HTTP request
            print("Error in the request:", e)

        except AttributeError as e:
            # Handle exceptions related to parsing the HTML content
            print("Error in parsing HTML:", e)

        except Exception as e:
            # Handle unexpected exceptions
            print("An unexpected error occurred:", e)

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
        link_tag = await product.query_selector('a.a-link-normal')
        span_tag = await product.query_selector('span.a-size-medium.a-color-base.a-text-normal')
        span_text = await span_tag.inner_text()
        arr_products.append(span_text)

        await select_product(page, product)
        return

async def select_product(category_page, product):
    link_tag = await product.query_selector('a.a-link-normal')
    await link_tag.click()
    await category_page.wait_for_load_state('load')
    await category_page.screenshot(path="amazon-product_1.png")
    # Parse the URL
    parsed_url = urlparse(category_page.url)

    # Extract the useful part (without query parameters)
    useful_part = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    global product_page_url
    product_page_url = useful_part

if __name__ == "__main__":
    asyncio.run(main(amazon_website, "Sony WH-1000MS4"))
