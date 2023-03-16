from chat_server import app, login, controllers, dao


app.add_url_rule('/auth', 'login', controllers.login)
app.add_url_rule('/oauth', 'login_oauth', controllers.login_oauth)
app.add_url_rule('/callback', 'oauth_callback', controllers.oauth_callback)

app.add_url_rule('/logout', 'logout', controllers.logout)


app.add_url_rule('/', 'home', controllers.home, methods=['get', 'post'])

app.add_url_rule("/search_user", 'search_user', controllers.search_user, methods=['post'])
app.add_url_rule("/get_mess_conv/<int:c_id>", 'get_mess_conv', controllers.get_mess_conv, methods=['get'])
app.add_url_rule("/add_conversation", 'add_conversation', controllers.add_conversation, methods=['post'])
app.add_url_rule("/get_list_receiver/<int:u_id>", 'get_list_receiver', controllers.get_list_receiver)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_attributes():
    return {
        'user_role': 'user'
    }


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)

