from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib
from werkzeug.utils import secure_filename

# ================= INIT =================
db = SQLAlchemy()

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

# ================= APP FACTORY =================
def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config['SECRET_KEY'] = 'super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['UPLOAD_FOLDER'] = 'uploads'

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)

    # ================= LOGIN =================
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    from app.models import User, Tutorial

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ================= ROUTES =================

    @app.route('/')
    def home():
        stats = {
            "total_waste_recycled": 120,
            "carbon_saved": 50,
            "active_users": 10,
            "points_earned": 600
        }
        return render_template('sustainability_dashboard.html', stats=stats)

    # ---------- AUTH ----------
    @app.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST':
            user = User(
                username=request.form['username'],
                password=hash_password(request.form['password'])
            )
            db.session.add(user)
            db.session.commit()
            flash("Registered successfully", "success")
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            user = User.query.filter_by(username=request.form['username']).first()

            if user and user.password == hash_password(request.form['password']):
                login_user(user)
                return redirect('/')

            flash("Invalid login", "danger")

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect('/')

    # ---------- PROFILE ----------
    @app.route('/profile')
    @login_required
    def profile():
        tutorials = Tutorial.query.filter_by(user=current_user.username).all()
        return render_template('profile.html', user=current_user, contributions=tutorials)

    # ---------- UPLOAD ----------
    @app.route('/upload', methods=['GET','POST'])
    @login_required
    def upload_tutorial():
        if request.method == 'POST':
            file = request.files.get('file')

            if file:
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)

                t = Tutorial(title=filename, video=filename, user=current_user.username)
                db.session.add(t)
                db.session.commit()

                flash("Uploaded!", "success")

        return render_template('upload_tutorial.html')

    # ---------- PREDICT ----------
    @app.route('/predict', methods=['GET','POST'])
    def predict():
        result = None

        if request.method == 'POST':
            value = float(request.form['value'])
            result = value * 0.5

        return render_template('predict.html', result=result)

    # ---------- AI CLASSIFY ----------
    from ml_model import predict_image

    @app.route('/classify', methods=['GET','POST'])
    def classify():
        result = None

        if request.method == 'POST':
            file = request.files.get('image')

            if file:
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)

                result = predict_image(path)

        return render_template('classify.html', result=result)

    # ---------- LEADERBOARD ----------
    @app.route('/leaderboard')
    def leaderboard():
        users = User.query.order_by(User.points.desc()).all()
        return render_template('leaderboard.html', users=users)

    return app