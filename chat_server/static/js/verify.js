const form = document.querySelector('form');
const inp = document.querySelector('.inp');
const email = document.querySelector('.title span').innerText;

document.body.onload = () => {
    inp.focus();
}
form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!inp.value) return
    await fetch(SERVER_URL + "/verify", {
        method: 'POST',
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            otp: inp.value,
            email: email
        })
    })
        .then(res => res.json())
        .then(data => {
            window.location.href = "/"
        })
});