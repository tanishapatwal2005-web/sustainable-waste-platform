from app import create_app, db
from app.models import User
import hashlib

app = create_app()

with app.app_context():
    # Create tables
    db.create_all()
    print("✅ Tables created")

    # Create admin
    existing = User.query.filter_by(username="admin").first()

    if not existing:
        admin = User(
            username="admin",
            password=hashlib.sha256("admin123".encode()).hexdigest(),
            role="admin",
            points=100
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created")
    else:
        print("⚠️ Admin already exists")