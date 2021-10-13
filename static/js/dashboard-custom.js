$(document).ready(function () {
    const pathname = document.location.href.toString()
    const sost_all = document.getElementsByClassName('click-li');
    for (const sost of sost_all) {
        const href = sost.childNodes[1].href.toString()
        if (pathname === href) {
            sost.className = 'click-li active'
        }
    }
})


function readyMain() {
    const triggers = document.getElementsByClassName('dashboard-responsive-nav-trigger')
    for (const trigger of triggers) {
        trigger.onclick = function (e) {
            const menuItems = document.getElementsByClassName('dashboard-nav')
            for (const menuItem of menuItems) {
                menuItem.classList.toggle('active')
            }
            e.preventDefault()
        }
    }
}

document.addEventListener("DOMContentLoaded", readyMain)