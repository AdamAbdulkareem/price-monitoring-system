function searchProductName(){
    const productName = document.getElementById("productName").value;
    console.log(`Searching for product: ${productName}`);
}

document.addEventListener("click", function (event){
    if (event.target && event.target.id === "searchButton"){
        searchProductName();
    }
});