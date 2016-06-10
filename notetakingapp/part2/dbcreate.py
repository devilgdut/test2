from main import db
import os

if( not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']))
db.create_all()