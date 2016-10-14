#coding=utf-8
'''
Created on 2016��9��13��

@author: huangning
'''

from flask import Flask,render_template,session,url_for
from flask import redirect,flash
from flask_bootstrap import Bootstrap
from datetime import datetime
# ...
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager


app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
manager = Manager(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:admin@192.168.1.237/hn'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['GET', 'POST'])
def index():

    form=NameForm()
    #return '<h1>Hello World!<h1>'
    #return redirect("http://www.hao123.com")
    #return render_template('index.html')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            flash('please register first!')
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:  
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
     
    return render_template('index.html',form=form, name=session.get('name'),known = session.get('known', False),current_time=datetime.utcnow())

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
    #manager.run()
    app.run(debug=True)
        