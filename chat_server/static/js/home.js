const searchInp = document.querySelector('.search-input')
const subSearch = document.querySelector('.sub-search')
const sidebar = document.querySelector('.left-list')
const sideContent = document.querySelector('.main-right__conversation')
const chatMain = document.querySelector('.main-right__chat')
const chatInp = document.querySelector('.chat-input')

let itemActiveSidebar = null

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
            <li data-id="${r.c_id}" data-user="${r.id}" class="left-item">
                <div class="left-item__avatar">
                    <img src="${r.avatar}"
                         alt="user">
                </div>
                <div class="left-item__info">
                    <div class="left-item__name">
                        ${r.fullname}
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
                    <div title="${r.created_at}" class="conversation-item ${r.sender == userId ? "author" : ""}">
                        ${decodeCaesar(r.content, r.c_id)}
                    </div>
                `
            }).join("")
            sideContent.dataset.id = c_id
            sideContent.innerHTML = htmls
            sideContent.scroll({
                top: sideContent.scrollHeight,
                behavior: 'smooth'
            })
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
            itemActiveSidebar = c_id
        }
    })

    if (flag) {
        const html = `
            <li data-id="${data.c_id}" data-user="${data.id}" class="left-item active">
                <div class="left-item__avatar">
                    <img src="${data.avatar}"
                         alt="user">
                </div>
                <div class="left-item__info">
                    <div class="left-item__name">
                        ${data.fullname}
                    </div>
                </div>
            </li>
        `
        sidebar.innerHTML += html
        await get_mess_conv_data(c_id)
    }

    subSearch.classList.remove('active')
}

// onlick sidebar
sidebar.onclick = async (e) => {
    const item = e.target.closest('.left-item')
    if (item) {
        await activeSidebar(item.dataset?.id)
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
            searchInp.value = ""
        }).catch(err => {
            console.log(err)
        })

}

// send message
chatMain.onsubmit = (e) => {
    e.preventDefault()
    const value = chatInp.value
    if (!value.trim() || !sideContent.dataset.id) return
    if (value.length > 100) return
    const receiver = document.querySelector(`.left-item[data-id='${sideContent.dataset.id}']`).dataset.user
    fetch(SERVER_URL + "/create_message", {
        method: 'POST',
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            c_id: sideContent.dataset.id,
            s_id: userId,
            r_id: receiver,
            content: encodeCaesar(value, sideContent.dataset.id)
        })
    })
        .then(res => res.json())
        .then(async data => {
            const res = data.data
            if (sideContent.dataset.id != res.c_id) return
            chatInp.value = ""
            chatInp.focus()
            const html = `
                <div title="${res.created_at}" class="conversation-item ${res.sender == userId ? "author" : ""}">
                    ${decodeCaesar(res.content, res.c_id)}
                </div>
            `
            sideContent.innerHTML += html
            sideContent.scroll({
                top: sideContent.scrollHeight,
                behavior: 'smooth'
            })
            socket.emit("send_message", res)
        }).catch(err => {
        console.log(err)
    })
}

socket.on("receive_message", data => {
    if (sideContent.dataset.id == data.c_id && data.receiver == userId) {
        const html = `
        <div title="${data.created_at}" class="conversation-item ${data.sender == userId ? "author" : ""}">
            ${decodeCaesar(data.content, data.c_id)}
        </div>
    `
        sideContent.innerHTML += html
        sideContent.scroll({
            top: sideContent.scrollHeight,
            behavior:'smooth'
        })
    }
})




