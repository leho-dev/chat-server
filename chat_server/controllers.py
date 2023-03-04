from flask import render_template, redirect
from flask_login import login_user

from chat_server.decorators import login_required
from chat_server import flow, dao, db
from chat_server.models import User


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
            password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
            fullname = user_oauth['name']
            image = user_oauth['picture']
            user = User(fullname=fullname, email=email)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect('/')
    except:
        return redirect("/auth")


@login_required
def home():
    return render_template('home.html')

