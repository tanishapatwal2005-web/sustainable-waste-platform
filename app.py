"""
AI-Based Sustainable Waste Platform (FINAL FIXED VERSION)
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import hashlib
import os

from chatbot import get_bot_response
from ml_model import predict_image

# ✅ IMPORT DB + MODELS
from app import db
from app.models import User, Tutorial


# ==================== APP INIT ====================
app = Flask(__name__, template_folder='app/templates')

app.config['SECRET_KEY'] = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ==================== LOGIN ====================
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# ✅ REQUIRED FIX (NO MORE ERROR)
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None


# ==================== HELPERS ====================
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()


# ==================== ROUTES ====================

# ✅ SINGLE HOME ROUTE (FIXED)
@app.route('/')
def home():
    stats = {
        "total_waste_recycled": 120,
        "carbon_saved": 50,
        "active_users": 10
    }
    return render_template('sustainability_dashboard.html', stats=stats)


# ---------- CHATBOT ----------
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    message = data.get("message")
    reply = get_bot_response(message)
    return jsonify({"response": reply})


# ---------- AUTH ----------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        existing = User.query.filter_by(username=request.form['username']).first()
        if existing:
            flash("Username already exists", "danger")
            return redirect(url_for('register'))

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
            return redirect(url_for('dashboard'))

        flash("Invalid login", "danger")

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# ---------- DASHBOARD ----------
@app.route('/dashboard')
@login_required
def dashboard():
    stats = {
        "points_earned": current_user.points,
        "co2_saved": current_user.points * 0.2
    }
    return render_template('dashboard.html', stats=stats)


# ---------- PROFILE ----------
@app.route('/profile')
@login_required
def profile():
    tutorials = Tutorial.query.filter_by(user=current_user.username).all()
    return render_template(
        'profile.html',
        user=current_user,
        waste_records=[],
        contributions=tutorials
    )


# ---------- CLASSIFY ----------
@app.route('/classify-waste', methods=['GET', 'POST'])
def classify_waste():
    result = None

    if request.method == 'POST':
        file = request.files.get('image')

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)

            result = predict_image(upload_path)

            if current_user.is_authenticated:
                current_user.points += 5
                db.session.commit()

    return render_template('classify.html', result=result)


# ---------- ATOM ECONOMY ----------
@app.route('/atom-economy', methods=['GET', 'POST'])
def atom_economy():
    result = None

    if request.method == 'POST':
        try:
            reactants = float(request.form['reactants_weight'])
            products = float(request.form['products_weight'])

            if reactants > 0:
                atom_val = round((products / reactants) * 100, 2)
                waste = round(100 - atom_val, 2)

                result = {
                    "atom_economy": atom_val,
                    "waste_percentage": waste
                }

        except:
            pass

    return render_template('atom_economy.html', result=result)


# ---------- PREDICT ----------
@app.route('/predict', methods=['GET','POST'])
def predict():
    result = None

    if request.method == 'POST':
        pop = float(request.form['population'])
        result = pop * 0.5

    return render_template('predict.html', prediction=result)


# ---------- GREEN SOLVENTS ----------
@app.route('/green-solvents')
def green_solvents():
    solvents = [
        {"name": "Water", "green_rating": "⭐⭐⭐⭐⭐"},
        {"name": "Ethanol", "green_rating": "⭐⭐⭐⭐"}
    ]
    return render_template('green_solvents.html', solvents=solvents)


# ---------- TUTORIALS ----------
@app.route('/tutorials')
def tutorials():
    return render_template('tutorials.html')


# ---------- UPLOAD ----------
@app.route('/upload-tutorial', methods=['GET','POST'])
@login_required
def upload_tutorial():
    if request.method == 'POST':
        t = Tutorial(
            title=request.form['title'],
            video=request.form['video'],
            user=current_user.username
        )
        db.session.add(t)
        db.session.commit()

        flash("Submitted", "info")
        return redirect(url_for('tutorials'))

    return render_template('upload_tutorial.html')


# ---------- COMMUNITY ----------
@app.route('/community')
def community_tutorials():
    tutorials = Tutorial.query.filter_by(approved=True).all()
    return render_template('community_tutorials.html', tutorials=tutorials)


# ---------- ADMIN ----------
@app.route('/admin/tutorials')
@login_required
def admin_tutorials():
    if not current_user.is_admin():
        return redirect('/')

    tutorials = Tutorial.query.all()
    return render_template('admin_tutorials.html', tutorials=tutorials)


# ---------- LEADERBOARD ----------
@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.points.desc()).all()
    return render_template('leaderboard.html', users=users)


# ==================== RUN ====================
if __name__ == '__main__':
    app.run(debug=True)