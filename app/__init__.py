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

    # ✅ REQUIRED
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
        "points_earned": 600   # ✅ ADD THIS (important)
    }
    return render_template('sustainability_dashboard.html', stats=stats)

   

    @app.route('/classify')
    def classify_waste():
        return "<h2>Classify Waste Page</h2>"

    @app.route('/predict')
    def predict():
        return "<h2>Prediction Page</h2>"

    @app.route('/atom')
    def atom_economy():
        return "<h2>Atom Economy Page</h2>"

    @app.route('/leaderboard')
    def leaderboard():
        return "<h2>Leaderboard Page</h2>"

    @app.route('/tutorials')
    def tutorials():
        return "<h2>Tutorials Page</h2>"

    @app.route('/community')
    def community_tutorials():
        return "<h2>Community Tutorials</h2>"

    @app.route('/upload')
    def upload_tutorial():
        return "<h2>Upload Tutorial</h2>"

    @app.route('/admin')
    def admin_tutorials():
        return "<h2>Admin Panel</h2>"

    @app.route('/profile')
    def profile():
        return "<h2>User Profile</h2>"

    @app.route('/login')
    def login():
        return "<h2>Login Page</h2>"

    @app.route('/register')
    def register():
        return "<h2>Register Page</h2>"

    @app.route('/logout')
    def logout():
        return "<h2>Logout</h2>"

    return app