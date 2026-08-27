// Cart check update

const products = document.querySelectorAll(".cart-product")
const cartCheck = document.querySelector(".cart-check")


function toRub(cost) {
    return cost.toLocaleString('ru-RU') + " ₽"
}

function checkUpdate() {
    let goodsCount = 0, totalCost = 0, resultCost = 0
    products.forEach((product) => {
        if (product.querySelector("input[type=checkbox]").checked) {
            let count = Number(product.querySelector(".counter > span").textContent)
            let previousCost = parseInt(product.querySelector(".previous-cost").textContent)
            let actualCost =  parseInt(product.querySelector(".cost").textContent)
            goodsCount += count; totalCost += previousCost * count; resultCost += actualCost * count
        }
    })

    cartCheck.querySelector(".cart-check-products > span.flex-grow-1").textContent = `Товары (${goodsCount})`
    cartCheck.querySelector(".cart-check-products > span:not(.flex-grow-1)").textContent = toRub(totalCost)
    cartCheck.querySelector(".cart-check-discount > span:not(.flex-grow-1)").textContent = "- " + toRub(totalCost - resultCost)
    cartCheck.querySelector(".cart-check-res > span:not(.flex-grow-1)").textContent = toRub(resultCost)
}


// Products selection

const CheckboxAll = document.getElementById("checkbox-all")
const checkboxes = Array.from(document.querySelectorAll("input[type=checkbox]:not(#checkbox-all)"))


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


// Products counter

const counters = document.querySelectorAll(".counter")

counters.forEach((counter, index) => {
    const buttons = counter.querySelectorAll("button")
    const span = counter.querySelector("span")

    buttons.forEach((button) => {
        button.onclick = function () {
            let count = Number(span.textContent)
            if (button.textContent === "+" && count < 9) count++
            else if (button.textContent === "–") {
                if (count > 1) count--
                else if (confirm("Вы уверены, что хотите удалить этот товар из корзины?")) {
                    products[index].remove()
                }
            }
            span.textContent = count.toString()
            checkUpdate()
        }
    })
})


document.getElementById('pay-btn').onclick = () => {
  window.location.href = window.location.origin + window.location.pathname + '/buy';
};
