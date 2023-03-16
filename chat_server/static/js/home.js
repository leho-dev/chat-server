const searchInp = document.querySelector('.search-input')
const subSearch = document.querySelector('.sub-search')
const userId = document.querySelector('.user-profile').dataset.id.split("-")[1]
const sidebar = document.querySelector('.left-list')
const sideContent = document.querySelector('.main-right__conversation')

// get sidebar
fetch(SERVER_URL + "/get_list_receiver/" + userId, {
    method: 'GET',
    headers: {
        "Content-type": "application/json"
    },
})
    .then(res => res.json())
    .then(data => {
        const htmls = data.data.map(r => {
            return `
            <li data-id="${r.c_id}" class="left-item">
                <div class="left-item__avatar">
                    <img src="${r.avatar}"
                         alt="user">
                </div>
                <div class="left-item__info">
                    <div class="left-item__name">
                        ${r.fullname}
                    </div>
                    <div class="left-item__last-mess">
                        ${r.last_mess}
                    </div>
                </div>
            </li>
        `
        }).join("")

        sidebar.innerHTML = htmls
    }).catch(err => {
    console.log(err)
})

const get_mess_conv_data = async (c_id) => {
    await fetch(SERVER_URL + "/get_mess_conv/" + c_id, {
        method: 'GET',
        headers: {
            "Content-type": "application/json"
        },
    })
        .then(res => res.json())
        .then(data => {
            const res = data.data
            const htmls = res.map(r => {
                return `
                    <div class="conversation-item ${r.sender == userId ? "author" : ""}">
                        ${r.content}
                    </div>
                `
            }).join("")
            sideContent.innerHTML = htmls
        })
}

// active sidebar
const activeSidebar = async (c_id, data) => {
    const listSidebar = document.getElementsByClassName('left-item');
    let flag
    if (data) {
        flag = 1
    }
    Array.from(listSidebar).forEach(item => {
        item.classList.remove('active')
        if (item.dataset.id == c_id) {
            flag = 0
            item.classList.add('active')
            get_mess_conv_data(c_id)
        }
    })

    if (flag) {
        const html = `
            <li data-id="${data.c_id}" class="left-item active">
                <div class="left-item__avatar">
                    <img src="${data.avatar}"
                         alt="user">
                </div>
                <div class="left-item__info">
                    <div class="left-item__name">
                        ${data.fullname}
                    </div>
                    <div class="left-item__last-mess">
                        ${data.last_mess || ""}
                    </div>
                </div>
            </li>
        `
        sidebar.innerHTML += html
        get_mess_conv_data(c_id)
    }

    subSearch.classList.remove('active')
}

// onlick sidebar
sidebar.onclick = (e) => {
    const item = e.target.closest('.left-item')
    if (item) {
        activeSidebar(item.dataset.id)
    }
}

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
                text: value.trim()
            })
        })
            .then(res => res.json())
            .then(data => {
                const res = data.data

                if (res.length) {
                    const htmls = res.map(r => {
                        return `
                        <li data-id=${r.id} class="sub-search__item">
                            <div class="search-item__img">
                                <img referrerpolicy="no-referrer" src=${r.avatar}
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

// click user subsearch
subSearch.onclick = async e => {
    const item = e.target.closest(".sub-search__item")
    const user2Id = item.dataset.id
    if (userId == user2Id) return
    if (!item) return

    await fetch(SERVER_URL + "/add_conversation", {
        method: 'POST',
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            user_1: userId,
            user_2: user2Id
        })
    })
        .then(res => res.json())
        .then(data => {
            const res = data.data
            const c_id = res.c_id
            activeSidebar(c_id, res)
        }).catch(err => {
            console.log(err)
        })

}


