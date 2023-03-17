from flask import render_template, redirect, request
from flask_login import login_user, logout_user
from chat_server.decorators import login_required, not_auth
from chat_server import flow, dao
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
        email = user_oauth['email']
        user = User.query.filter_by(email=email).first()
        if user is None:
            fullname = user_oauth['name']
            avatar = user_oauth['picture']
            user = dao.create_user(fullname, email, avatar)
        login_user(user)
        return redirect('/verify')
    except:
        return redirect("/auth")


@login_required
def home():
    return render_template('home.html')


def search_user():
    data = request.get_json()
    user_list = dao.get_list_user_by_text(text=data['text'])
    return {
        "status": 200,
        "data": user_list
    }


def get_list_receiver(u_id):
    data = dao.get_list_receiver(u_id)
    return {
        "status": 200,
        "data": data
    }


def add_conversation():
    data = request.get_json()
    conv = dao.create_conv_json(data['user_1'], data['user_2'])
    return {
        "status": 200,
        "data": conv
    }


def get_mess_conv(c_id):
    data = dao.get_mess_conv_json(c_id)
    return {
        "status": 200,
        "data": data
    }

def create_message():
    data = request.get_json()
    mess = dao.create_message_json(data['c_id'], data['s_id'], data['r_id'], data['content'])
    return {
        "status": 200,
        "data": mess
    }


def logout():
    logout_user()
    return redirect('/auth')
