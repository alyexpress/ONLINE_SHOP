const productID = document.querySelector(".product").dataset.productId
const toCartBtn = document.querySelector(".product button.to-cart")
const productCounter = document.querySelector(".product .counter")
const counterSpan = productCounter.querySelector("span")
let productCount = 0;


document.addEventListener("DOMContentLoaded", function () {
    let count = getCookie(productID)
    if (Number.isFinite(Number(count))) {
        productCount = parseInt(count)
        counterSpan.textContent = productCount.toString()
        productCounter.classList.remove("d-none")
    } else toCartBtn.classList.remove("d-none")
})

toCartBtn.onclick = function () {
    toCartBtn.classList.add("hide")
    setTimeout(function () {
        toCartBtn.classList.add("d-none")
        toCartBtn.classList.remove("hide")
        productCounter.classList.remove("d-none")
    }, 300)
    productCount = 1
    setCookie(productID, productCount)
}

productCounter.querySelectorAll("button").forEach((button) => {
    button.onclick = function () {
        if (button.textContent === "+" && productCount < 9) productCount++
        else if (button.textContent === "–" ) {
            if (productCount > 1) productCount--
            else if (confirm("Вы уверены, что хотите удалить этот товар из корзины?")) {
                productCounter.classList.add("d-none")
                toCartBtn.classList.remove("d-none")
                delCookie(productID)
                productCount--
            }
        }
        if (0 < productCount) {
            counterSpan.textContent = productCount.toString()
            setCookie(productID, productCount)
        }
    }
})