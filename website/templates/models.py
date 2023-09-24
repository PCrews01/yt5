from website import DB

class Users(DB.Model):
	id = DB.Column(DB.Integer, primary_key=True)
	name = DB.Column(DB.String(50))
	email = DB.Column(DB.String(50), unique=True)

