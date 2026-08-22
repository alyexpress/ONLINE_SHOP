// Cart check update

function checkUpdate() {

}


// Products selection

const CheckboxAll = document.getElementById("checkbox-all")
const checkboxes = Array.from(document.querySelectorAll("input[type=checkbox]:not(#checkbox-all)"))


CheckboxAll.onchange = function () {
    checkboxes.forEach((checkbox) => {
        checkbox.checked = CheckboxAll.checked
    })
}

checkboxes.forEach((checkbox) => {
    checkbox.onchange = function () {
        CheckboxAll.checked = checkboxes.every(x => x.checked)
    }
})


// Products counter

const products = document.querySelectorAll(".cart-product")
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
        }
    })
})
