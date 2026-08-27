function setCookie(key, val) {
    document.cookie = `${key}=${val};path=/`
    updateHeader()
}

function getCookie(key) {
	let matches = document.cookie.match(new RegExp("(?:^|; )" + key.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
	return matches ? decodeURIComponent(matches[1]) : undefined;
}

function delCookie(key) {
    document.cookie = `${key}=;path=/;max-age=-1`
    updateHeader()
}

function updateHeader(prefix="product_") {
    const span = document.querySelector("header .navigation-bar > a > span")
    let totalCount = 0;

    document.cookie.split(';').forEach((cookie) => {
        const [name, value] = cookie.trim().split('=');
        if (name && name.startsWith(prefix)) totalCount += parseInt(value)
    })

    if (totalCount > 0) span.classList.remove("d-none")
    else span.classList.add("d-none")

    span.textContent = totalCount.toString()
}

document.addEventListener("DOMContentLoaded", function () {
    updateHeader()
})