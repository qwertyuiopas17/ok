from enhanced_database_models import db, Doctor, init_database
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/enhanced_chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Initialize database if needed
    init_database(app)
    doctors = Doctor.query.all()
    print('Doctors in database:')
    for d in doctors:
        print(f'ID: {d.doctor_id}, Name: {d.full_name}, Active: {d.is_active}, Has Password: {d.password_hash is not None}')