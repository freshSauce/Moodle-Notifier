from database import db


class Users(db.Model):
    telegram_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    sess_key = db.Column(db.String, nullable=False)
    cookies = db.Column(db.PickleType, nullable=False)


def create_tables(app, drop=False):
    if not drop:
        with app.app_context():
            db.create_all()
    else:
        with app.app_context():
            db.drop_all()
            db.create_all()
