const avtUser = document.querySelector('.user-profile__img img')
const searchInp = document.querySelector('.search-input')
const subSearch = document.querySelector('.sub-search')

avtUser.src = avtUser.getAttribute("lazy-src");
avtUser.removeAttribute("lazy-src");

// debounce search
let timerId

searchInp.oninput = (e) => {
    if (timerId) {
        clearTimeout(timerId)
        timerId = null
    }

    timerId = setTimeout(async () => {
        const value = searchInp.value

        if (!value.trim()) {
            subSearch.classList.remove('active')
            return
        }
        fetch(SERVER_URL + "/search_user", {
            method: 'POST',
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify({
                text: value
            })
        })
        .then(res => res.json())
        .then(data => {
            const res = data.data

            if (res.length) {
                const htmls = res.map(r => {
                    return `
                        <li class="sub-search__item">
                            <div class="search-item__img">
                                <img src=${r.avatar}
                                     alt="user-avatar">
                            </div>
                            <div class="search-item__info">
                                <div class="search-item__name">
                                    ${r.fullname}
                                </div>
                            </div>
                        </li>
                    `
                }).join("")

                subSearch.classList.add('active')
                subSearch.innerHTML = htmls;
            } else {
                subSearch.classList.remove('active')
            }
        }).catch(err => {
            console.log(err)
        })
    }, 500)
}