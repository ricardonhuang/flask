#coding=utf-8
'''
Created on 2016��9��13��

@author: huangning
'''

from flask import Flask,render_template
from flask import redirect
from flask_bootstrap import Bootstrap
from datetime import datetime
# ...
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    #return '<h1>Hello World!<h1>'
    #return redirect("http://www.hao123.com")
    #return render_template('index.html')
    return render_template('index.html',current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/user/<name>')
def user(name):
    #return '<h1>Hello, %s!</h1>' % name
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)

        