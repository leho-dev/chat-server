from flask import render_template, redirect, session
from flask_login import login_user, logout_user

from chat_server.decorators import login_required, not_auth
from chat_server import flow, dao, db
from chat_server.models import User


@not_auth
def login():
    return render_template('index.html')


def login_oauth():
    authorization_url, state = flow.authorization_url()
    return redirect(authorization_url)


def oauth_callback():
    try:
        user_oauth = dao.get_user_oauth()
        print(user_oauth)
        email = user_oauth['email']
        user = User.query.filter_by(email=email).first()
        if user is None:
            import hashlib
            fullname = user_oauth['name']
            avatar = user_oauth['picture']
            user = User(fullname=fullname, email=email, avatar=avatar)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect('/')
    except:
        return redirect("/auth")


@login_required
def home():
    return render_template('home.html')


def logout():
    logout_user()
    return redirect('/auth')

