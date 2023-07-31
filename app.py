from flask import Flask
from db.connection import db
from flask_login import LoginManager
login_manager = LoginManager()


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite3"
app.config['SECRET_KEY'] = 'the random string'    

db.init_app(app)

login_manager.init_app(app)

app.app_context().push()


from application.models import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

from application.controller import *



if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(host='localhost',port=5000,debug=True)



