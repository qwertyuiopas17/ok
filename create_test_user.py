from chatbot import app, db, User
import bcrypt

def create_test_user():
    with app.app_context():
        # Check if user exists
        existing = User.query.filter_by(patient_id='PAT000010').first()
        if existing:
            print("User PAT000010 already exists")
            return

        # Create test user
        hashed_password = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt())
        test_user = User(
            patient_id='PAT000010',
            email='test@example.com',
            full_name='Test User',
            phone_number='1234567890',
            village='Test Village',
            district='Test District',
            state='Punjab',
            pincode='123456',
            preferred_language='en',
            password_hash=hashed_password.decode('utf-8'),
            is_active=True
        )
        db.session.add(test_user)
        db.session.commit()
        print("Created test user PAT000010")

if __name__ == "__main__":
    create_test_user()