from flask import Flask, render_template
from flask_login import LoginManager, AnonymousUserMixin

class DummyUser(AnonymousUserMixin):
    def is_admin(self):
        return False

def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config['SECRET_KEY'] = 'super-secret-key'

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.anonymous_user = DummyUser

    @login_manager.user_loader
    def load_user(user_id):
        return None

    # ================= ROUTES ================= #

    @app.route('/')
    def home():
        stats = {
            "total_waste_recycled": 120,
            "carbon_saved": 50,
            "active_users": 10,
            "points_earned": 600
        }
        return render_template('sustainability_dashboard.html', stats=stats)

    @app.route('/classify')
    def classify_waste():
        return render_template('classify.html')

    @app.route('/predict')
    def predict():
        return render_template('predict.html')

    @app.route('/atom')
    def atom_economy():
        return render_template('atom_economy.html')

    @app.route('/leaderboard')
    def leaderboard():
        return render_template('leaderboard.html')

    @app.route('/tutorials')
    def tutorials():
        return render_template('tutorials.html')

    @app.route('/community')
    def community_tutorials():
        return render_template('community_tutorials.html')

    @app.route('/upload')
    def upload_tutorial():
        return render_template('upload_tutorial.html')

    @app.route('/admin')
    def admin_tutorials():
        return render_template('admin_tutorials.html')

    @app.route('/profile')
    def profile():
        return render_template('profile.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        return render_template('logout.html')

    return app