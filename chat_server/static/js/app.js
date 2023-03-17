const SERVER_URL = 'http://localhost:5001'

// encode
const encodeCaesar = (text, id) => {
    const res = []
    const key = id % 26
    text.split("").forEach(i => {
        if (i >= "a" && i <= "z" || i >= "A" && i <= "Z" || i >= "0" && i <= "9") {
            let value = i.charCodeAt(0) + key
            if (i >= "a" && i <= "z" && value > 'z'.charCodeAt(0) ||
                i >= "A" && i <= "Z" && value > 'Z'.charCodeAt(0)) {
                    value = value - 26
            }

            if (i >= "0" && i <= "9" && value > '9'.charCodeAt(0)) {
                    while (value > '9'.charCodeAt(0)) {
                        value = value - 10
                    }
            }
            res.push(String.fromCharCode(value))
        } else {
            res.push(i)
        }
    })
    return res.join("")
}

// decode
const decodeCaesar = (text, id) => {
    const res = []
    const key = id % 26
    text.split("").forEach(i => {
        if (i >= "a" && i <= "z" || i >= "A" && i <= "Z" || i >= "0" && i <= "9") {
            let value = i.charCodeAt(0) - key
            if (i >= "a" && i <= "z" && value < 'a'.charCodeAt(0) ||
                i >= "A" && i <= "Z" && value < 'A'.charCodeAt(0)) {
                    value = value + 26
            }

            if (i >= "0" && i <= "9" && value < '0'.charCodeAt(0)) {
                    while (value < '0'.charCodeAt(0)) {
                        value = value + 10
                    }
            }
            res.push(String.fromCharCode(value))
        } else {
            res.push(i)
        }
    })
    return res.join("")
}
