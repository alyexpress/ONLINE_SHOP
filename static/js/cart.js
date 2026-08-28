// Cart check update

let products = document.querySelectorAll(".cart-product")
let cartCheck = document.querySelector(".cart-check")


function updateCartProducts() {
    products = document.querySelectorAll(".cart-product")
    cartCheck = document.querySelector(".cart-check")
    CheckboxAll = document.getElementById("checkbox-all")
    checkboxes = Array.from(document.querySelectorAll("input[type=checkbox]:not(#checkbox-all)"))
    counters = document.querySelectorAll(".cart-product .counter")
    setCart()
}

function toRub(cost) {
    return cost.toLocaleString('ru-RU') + " ₽"
}

function checkUpdate() {
    let goodsCount = 0, totalCost = 0, resultCost = 0
    products.forEach((product) => {
        if (product.querySelector("input[type=checkbox]").checked) {
            let count = Number(product.querySelector(".counter > span").textContent)
            let actualCost =  parseInt(product.querySelector(".cost").textContent.replace(" ", ""))
            let previousCost = product.querySelector(".previous-cost")
            if (previousCost === null) previousCost = actualCost
            else previousCost = parseInt(previousCost.textContent.replace(" ", ""))
            goodsCount += count; totalCost += previousCost * count; resultCost += actualCost * count
        }
    })

    cartCheck.querySelector(".cart-check-products > span.flex-grow-1").textContent = `Товары (${goodsCount})`
    cartCheck.querySelector(".cart-check-products > span:not(.flex-grow-1)").textContent = toRub(totalCost)
    cartCheck.querySelector(".cart-check-discount > span:not(.flex-grow-1)").textContent = "- " + toRub(totalCost - resultCost)
    cartCheck.querySelector(".cart-check-res > span:not(.flex-grow-1)").textContent = toRub(resultCost)
}


document.addEventListener("DOMContentLoaded", function () {
    checkUpdate(); setCart();
})


// Products selection

let CheckboxAll = document.getElementById("checkbox-all")
let checkboxes = Array.from(document.querySelectorAll("input[type=checkbox]:not(#checkbox-all)"))
let counters = document.querySelectorAll(".cart-product .counter")


function setCart() {
    CheckboxAll.onchange = function () {
        checkboxes.forEach((checkbox) => {
            checkbox.checked = CheckboxAll.checked
        })
        checkUpdate()
    }

    checkboxes.forEach((checkbox) => {
        checkbox.onchange = function () {
            CheckboxAll.checked = checkboxes.every(x => x.checked)
            checkUpdate()
        }
    })

    counters.forEach((counter, index) => {
        const span = counter.querySelector("span")
        const productID = counter.dataset.productId

        counter.querySelectorAll("button").forEach((button) => {
            button.onclick = function () {
                let count = Number(span.textContent)
                if (button.textContent === "+" && count < 9) count++
                else if (button.textContent === "–") {
                    if (count > 1) count--
                    else if (confirm("Вы уверены, что хотите удалить этот товар из корзины?")) {
                        count--; span.textContent = count.toString(); checkUpdate()
                        delCookie(productID); products[index].remove()
                        const cartProd = document.querySelector(`.product-grid > .col[data-product-id="${productID}"]`)
                        cartProd.querySelector(".counter").classList.add("d-none")
                        cartProd.querySelector("button").classList.remove("d-none")
                        // if (cartProd !== undefined) cartProd.querySelector(".counter > span").textContent = count.toString()

                    }
                }
                if (0 < count) {
                    span.textContent = count.toString()
                    checkUpdate(); setCookie(productID, count)

                    const cartProd = document.querySelector(`.product-grid > .col[data-product-id="${productID}"]`)
                    if (cartProd !== null) cartProd.querySelector(".counter > span").textContent = count.toString()
                }
            }
        })
    })
}

document.getElementById('pay-btn').onclick = () => {
  window.location.href = window.location.origin + window.location.pathname + '/buy'
}
