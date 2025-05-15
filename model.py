from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')