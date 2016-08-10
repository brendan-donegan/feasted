#!/usr/bin/python3

import os

import flask
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_migrate import (
    Migrate,
    MigrateCommand,
)
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)


basedir = os.path.abspath(os.path.dirname(__file__))


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'flotsam&jetsom'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dghfuqmyebssye:PzwnEwijNWlSyq6a6HNSjBMP8T@ec2-23-23-208-32.compute-1.amazonawscom:5432/dea6g6c5r1ostb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager = Manager(app)
manager.add_command("shell", Shell(make_context=make_shell_context))
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role {}>'.format(self.name)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            flask.session['known'] = False
        else:
            flask.session['known'] = True
        flask.session['name'] = form.name.data
        form.name.data = ''
        return flask.redirect(flask.url_for('index'))
    user_agent = flask.request.headers.get('User-Agent')
    return flask.render_template(
        'index.html',
        form=form,
        name=flask.session.get('name'),
        known=flask.session.get('known'),
        user_agent=user_agent,
    )

@app.route('/user/<name>')
def user(name):
    if name not in ['Tyler', 'Brendan']:
        flask.abort(404)
    return flask.render_template('user.html', name=name)

@app.route('/help')
def help():
    return flask.render_template('help.html')

if __name__ == '__main__':
    manager.run()
