from flask import render_template
from chat_server.decorators import login_required


def login():
    return render_template('index.html')


@login_required
def home():
    return render_template('home.html')

