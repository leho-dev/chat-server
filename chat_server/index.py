from chat_server import app, login, controllers, dao, socket
from flask import request

app.add_url_rule('/auth', 'login', controllers.login)
app.add_url_rule('/oauth', 'login_oauth', controllers.login_oauth)
app.add_url_rule('/callback', 'oauth_callback', controllers.oauth_callback)

app.add_url_rule('/logout', 'logout', controllers.logout)

app.add_url_rule('/', 'home', controllers.home, methods=['get', 'post'])
app.add_url_rule('/verify', 'verify', controllers.verify, methods=['get', 'post'])

app.add_url_rule("/search_user", 'search_user', controllers.search_user, methods=['post'])
app.add_url_rule("/get_mess_conv/<int:c_id>", 'get_mess_conv', controllers.get_mess_conv, methods=['get'])
app.add_url_rule("/add_conversation", 'add_conversation', controllers.add_conversation, methods=['post'])
app.add_url_rule("/create_message", 'create_message', controllers.create_message, methods=['post'])
app.add_url_rule("/get_list_receiver/<int:u_id>", 'get_list_receiver', controllers.get_list_receiver)

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

@app.context_processor
def common_attributes():
    return {
        'user_role': 'user'
    }


# socket
listSocket = []

@socket.on('client_connect')
def handle_client_conn(data):
    global listSocket
    listSocket.append({
        'id': data['id'],
        'socketId': request.sid,
    })

@socket.on("disconnect")
def handle_disconnect():
    global listSocket
    listSocket = list(filter(lambda obj: obj['socketId'] != request.sid, listSocket))

@socket.on("send_message")
def handle_message(data):
    socket.emit("receive_message", data)

if __name__ == '__main__':
    # ssl_context = ('./ssl/cert.pem', './ssl/key.pem')
    socket.run(app, allow_unsafe_werkzeug=True, port=5001, debug=True, host="localhost")

