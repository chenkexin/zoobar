from flask import g, render_template, request
from login import requirelogin
from debug import *

@catch_err
@requirelogin
def index():
    if 'profile_update' in request.form:
        g.user.person.profile = request.form['profile_update']
    return render_template('index.html')
