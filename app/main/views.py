from flask import render_template, session, redirect, request, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    user_agent = request.headers.get('User-Agent')
    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        known=session.get('known'),
        user_agent=user_agent,
    )

@main.route('/help')
def help():
    return render_template('help.html')
