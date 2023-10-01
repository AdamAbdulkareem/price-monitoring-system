function searchProductName(productName) {
    // Define the data to be sent in the POST request
    const data = {
        amazon_website: "https://www.amazon.com",
        product_name: productName
    };

    // Define the URL of your Flask endpoint
    const url = "http://localhost:5000/scrape_amazon";

    // Define the options for the fetch request
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    };

    // Make the fetch request
    fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            // Update the HTML content with the received JSON data
            const productList = document.getElementById("productList");
            productList.innerHTML = "";
            // Iterate over the products and create list items
            data.products.forEach(product =>{
                const listItem = document.createElement("li");

                // Create an image element
                const image = document.createElement("img");
                image.src = product.product_img_url;
                // Create a span element for the product title
                const titleSpan = document.createElement("span");
                titleSpan.textContent = product.product_title;

                listItem.appendChild(image);
                listItem.appendChild(titleSpan);
                listItem.setAttribute("data-asin", product.product_id);

                productList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error("Error:", error);
        });
    console.log(`Searching for product: ${productName}`);
}


function scrapeAmazonProduct(dataAsin){
    // Define the data to be sent in the POST request
    const data = {
        data_asin : dataAsin
    };

    const url = "http://localhost:5000/scrape_amazon_product";

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    };

    fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(

        )
}

document.addEventListener("DOMContentLoaded", function(){
    const productList = document.getElementById("productList");
    productList.addEventListener("click", function(event){
        // Check if the clicked element is an <li>
        if (event.target.tagName == "LI"){
            // Extract the data-asin attribute value from the clicked <li>
            const dataAsin = event.target.getAttribute("data-asin");
            scrapeAmazonProduct(dataAsin)
        }
    })
    }
)

document.addEventListener("DOMContentLoaded", function(){
    const searchButton = document.getElementById("searchButton");
    // Add a click event listener to the search button
    searchButton.addEventListener("click", function(){
        const productName = document.getElementById("productName").value;
        searchProductName(productName);
    });
});