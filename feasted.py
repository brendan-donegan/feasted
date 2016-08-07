#!/usr/bin/python3

import flask
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

app = flask.Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    user_agent = flask.request.headers.get('User-Agent')
    return flask.render_template('index.html', user_agent=user_agent)

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
