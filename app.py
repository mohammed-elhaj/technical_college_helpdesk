# File: app.py
from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
from routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        # Create admin user if not exists
        admin = User.query.filter_by(email='admin@college.edu').first()
        if not admin:
            from werkzeug.security import generate_password_hash
            admin = User(
                full_name='Admin User',
                email='admin@college.edu',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)