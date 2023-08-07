from flask import current_app as app
from flask import render_template,request,redirect,url_for
from application.models import *
from db.connection import db
from flask_login import login_user,login_required,current_user

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

            if user.is_admin:
            # return 'login successfull'
                return redirect('/dashboard')
            else:
                return redirect('/dashboard_user')
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


@app.route('/delete_category/<id>',methods=['GET'])
@login_required
def delete_category(id):
    category = Category.query.filter_by(id=id).first()
    if category:
        db.session.delete(category)
        db.session.commit()
    return redirect('/dashboard')


@app.route('/update_category/<id>',methods=['GET'])
@login_required
def update_category(id):
    form = request.form
    category = Category.query.filter_by(id=id).first()
    category.name = form['name']
    db.session.commit()
    return redirect('/dashboard')


@app.route('/products/<category>',methods=['GET'])
@login_required
def get_products(category):
    category = Category.query.filter_by(name=category).first()
    if category:
        products = Product.query.filter_by(category_id=category.id).all()

        return render_template('products_manager.html',products=products, category=category)

@app.route('/add_products/<category>',methods=['POST'])
@login_required
def add_product(category):
    form = request.form
    category = Category.query.filter_by(name=category).first()
    product = Product(name=form['name'],Manu_date=form['date'],rate=form['rate'],category_id=category.id)

    db.session.add(product)
    db.session.commit()

    products = Product.query.filter_by(category_id=category.id).all()

    return render_template('products_manager.html',products=products,category=category)


@app.route('/delete_products/<id>',methods=['GET'])
@login_required
def delete_product(id):
    product = Product.query.filter_by(id=id).first()
    category = Category.query.filter_by(id=product.category_id).first()
    

    if product:
        db.session.delete(product)
        db.session.commit()

    return redirect(url_for('get_products', category=category.name))


@app.route('/update_category/<id>',methods=['GET'])
@login_required
def update_product(id):
    form = request.form
    product = Product.query.filter_by(id=id).first()
    category = Category.query.filter_by(id=product.category_id).first()
    product.name = form['name']
    product.Manu_date=form['date']
    product.rate=form['rate']
    product.category_id=category.id
    db.session.commit()
    return redirect('/dashboard')

@app.route('/products_user/<category>',methods=['GET'])
@login_required
def get_products_user(category):
    category = Category.query.filter_by(name=category).first()
    if category:
        products = Product.query.filter_by(category_id=category.id).all()

        return render_template('products_user.html',products=products, category=category)

@app.route('/dashboard_user',methods=['GET','POST'])
@login_required
def dashboard_user():
    categories = Category.query.all()
    return render_template('dashboard_user.html',categories=categories)


@app.route('/add_cart/<id>',methods=['GET'])
@login_required
def add_cart(id):
    product = Product.query.filter_by(id=id).first()
    category = Category.query.filter_by(id=product.category_id).first()
    cart = Cart(user_id=current_user.id,product_id=id)
    db.session.add(cart)
    db.session.commit()
    products = Product.query.filter_by(category_id=category.id).all()
    return render_template('products_user.html',products=products)


@app.route('/view_cart',methods=['GET'])
@login_required
def view_cart():

    # user = User.query.filter_by(id=current_user.id).first()
    carts = Cart.query.filter_by(user_id=current_user.id)
    temp = []
    for cart in carts:
        product = Product.query.filter_by(id=cart.product_id).first()
        temp.append(product)

    return render_template('cart.html',products=temp)


    