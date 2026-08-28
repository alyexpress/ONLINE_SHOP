async function loadJSON(url) {
    const response = await fetch(url)
    return await response.json()
}

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

    btn.onclick = async function () {
        btn.classList.add("d-none")
        counter.classList.remove("d-none")
        count = 1
        setCookie(productID, count)
        const data = await loadJSON(`/api/product/${productID}`)
        document.querySelector(".cart-products > div").innerHTML += `
                    <div class="cart-product d-flex row">
                        <label class="d-flex align-items-center checkbox-body">
                            <input type="checkbox" checked hidden>
                            <span class="checkbox">
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-check" viewBox="0 0 16 16">
                                    <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425z"></path>
                                </svg>
                            </span>
                        </label>
                        <div class="col-2"><img src="/static/${ data["cover_src"] }" alt=""></div>
                        <div class="col-6">
                            <a href="/product/${ data["id"] }" class="flex-grow-1">${ data["name"] }</a>
                            <div class="d-flex align-items-center">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                                    <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"></path>
                                </svg>
                                <span>${ data["rating"] }</span>
                                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-person-fill" viewBox="0 0 16 16">
                                    <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6"></path>
                                </svg>
                                <span class="seller-name">${ data["shop_name"] }</span>
                            </div>
                        </div>
                        <div class="col-2">
                            <span class="cost">${ data["price"] }</span>
                            ${ data["discount"] != null ? `<span class="previous-cost">${ data["previous_price"] }</span>` : "" }
                        </div>
                        <div class="col-2">
                            <div class="counter" data-product-id="product_${ data["id"] }">
                                <button>–</button>
                                <span>1</span>
                                <button>+</button>
                            </div>
                        </div>
                    </div>`
        updateCartProducts(); checkUpdate()
    }

    counter.querySelectorAll("button").forEach((button) => {
        button.onclick = function () {
            count = parseInt(counterSpan.textContent)
            if (button.textContent === "+" && count < 9) count++
            else if (button.textContent === "–") {
                if (count > 1) count--
                else if (confirm("Вы уверены, что хотите удалить этот товар из корзины?")) {
                    counter.classList.add("d-none")
                    btn.classList.remove("d-none")
                    count--; delCookie(productID)
                    const cartProd = document.querySelector(`.cart-product:has(.counter[data-product-id="${ productID }"])`)
                    cartProd.querySelector(".counter > span").textContent = "0"; checkUpdate(); cartProd.remove()
                }
            }
            if (0 < count) {
                counterSpan.textContent = count.toString()
                setCookie(productID, count)

                let cartElement = document.querySelector(`.cart-product:has(.counter[data-product-id="${ productID }"])`)
                cartElement.querySelector(".counter > span").textContent = count.toString()
                checkUpdate()
            }
        }
    })
})