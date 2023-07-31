from flask import current_app as app
from flask import render_template,request,redirect
from application.models import *
from db.connection import db
from flask_login import login_user,login_required

@app.route('/',methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/validate',methods=['POST'])
def validate():
    form = request.form
    user = User.query.filter_by(email=form['email']).first()
    if user:
        if user.password == form['password']:
            login_user(user)
            return 'login successfull'
        else:
            return 'Scammer'
    return 'Scammer'

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard_manager():
    categories = Category.query.all()
    return render_template('dashboard_manager.html',categories=categories)

@app.route('/add_category',methods=['POST'])
@login_required
def add_category():
    form = request.form
    category = Category(nProd=0,name=form['category'])
    db.session.add(category)
    db.session.commit()
    return redirect('/dashboard')


    