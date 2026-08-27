document.querySelectorAll(".product-grid > .col").forEach((product) => {
    const productID = product.dataset.productId
    const btn = product.querySelector("button")
    const counter = product.querySelector(".counter")
    const counterSpan = counter.querySelector("span")
    let count = 0

    document.addEventListener("DOMContentLoaded", function () {
        let cookieCount = getCookie(productID)
        if (Number.isFinite(Number(cookieCount))) {
            count = parseInt(cookieCount)
            counterSpan.textContent = count.toString()
            btn.classList.add("d-none")
            counter.classList.remove("d-none")
        }
    })

    btn.onclick = function () {
        btn.classList.add("d-none")
        counter.classList.remove("d-none")
        count = 1
        setCookie(productID, count)
    }

    counter.querySelectorAll("button").forEach((button) => {
        button.onclick = function () {
            if (button.textContent === "+" && count < 9) count++
            else if (button.textContent === "–") {
                if (count > 1) count--
                else if (confirm("Вы уверены, что хотите удалить этот товар из корзины?")) {
                    counter.classList.add("d-none")
                    btn.classList.remove("d-none")
                    count--; delCookie(productID)
                }
            }
            if (0 < count) {
                counterSpan.textContent = count.toString()
                setCookie(productID, count)
            }
        }
    })

})