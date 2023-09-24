from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager
import random
DB = SQLAlchemy()
DB_NAME = "yt5.db"
def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = '**CHANGE ME IMMEDIATELY**'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	DB.init_app(app)
	from .templates.views import views
	from .templates.auth import auth

	app.register_blueprint(views, url_prefix="/")
	app.register_blueprint(auth, url_prefix="/")

	from .templates.models import Users
	if not path.exists('website/' + DB_NAME):
		with app.app_context():
			DB.create_all()
			print('Database created')	
	login_manager = LoginManager()

	login_manager.login_view = 'auth.login'

	login_manager.init_app(app)


	@login_manager.user_loader

	def load_user(id):
		return Users.query.get(int(id))
	return app

