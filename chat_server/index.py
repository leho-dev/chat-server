from chat_server import app, login, controllers, dao


app.add_url_rule('/auth', 'login', controllers.login, methods=['get', 'post'])
app.add_url_rule('/oauth', 'login_oauth', controllers.login_oauth)
app.add_url_rule('/callback', 'oauth_callback', controllers.oauth_callback)


app.add_url_rule('/', 'home', controllers.home, methods=['get', 'post'])


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

