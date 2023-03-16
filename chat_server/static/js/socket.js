const userId = document.querySelector('.user-profile').dataset.id.split("-")[1]
const socket = io();
socket.connect('http://localhost:5001/')

socket.on('connect', function () {
    socket.emit('client_connect',{
        id: userId,
    });
});

socket.on('disconnect', function () {
    socket.emit('client_disconnect',{
        id: userId,
    });
});