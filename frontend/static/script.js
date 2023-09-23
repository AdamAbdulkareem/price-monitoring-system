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
            console.log("Scraping response:", data);
        })
        .catch(error => {
            console.error("Error:", error);
        });

    console.log(`Searching for product: ${productName}`);
}



document.addEventListener("DOMContentLoaded", function(){
    const searchButton = document.getElementById("searchButton");
    // Add a click event listener to the search button
    searchButton.addEventListener("click", function(){
        const productName = document.getElementById("productName").value;
        searchProductName(productName);
    });
});