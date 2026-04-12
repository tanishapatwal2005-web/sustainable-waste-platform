"""
AI-Based Sustainable Waste Platform (FINAL FIXED VERSION)
"""
from flask import request, jsonify
from chatbot import get_bot_response
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app import create_app, db
from app.models import User, Tutorial
import hashlib
import os
from werkzeug.utils import secure_filename

# ✅ AI MODEL (FIXED)
from ml_model import predict_image

app = create_app()

# ✅ UPLOAD FOLDER FIX
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ==================== LOGIN ====================
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

# ==================== ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')

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
    return render_template('profile.html',
                           user=current_user,
                           waste_records=[],
                           contributions=tutorials)

# ---------- CLASSIFY (AI) ----------
@app.route('/classify-waste', methods=['GET', 'POST'])
def classify_waste():
    result = None

    if request.method == 'POST':
        file = request.files.get('image')

        if file and file.filename != '':
            filename = secure_filename(file.filename)

            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)

            # 🔥 AI Prediction
            result = predict_image(upload_path)

            # ✅ SAVE POINTS (FIXED)
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
                atom_economy_value = round((products / reactants) * 100, 2)
                waste = round(100 - atom_economy_value, 2)

                # 🎯 Rating logic
                if atom_economy_value >= 90:
                    rating = "Excellent"
                    color = "success"
                    message = "Highly sustainable reaction with minimal waste."
                elif atom_economy_value >= 70:
                    rating = "Good"
                    color = "primary"
                    message = "Good efficiency with moderate waste."
                elif atom_economy_value >= 50:
                    rating = "Average"
                    color = "warning"
                    message = "Average efficiency. Consider optimization."
                else:
                    rating = "Poor"
                    color = "danger"
                    message = "Low efficiency. High waste production."

                result = {
                    "atom_economy": atom_economy_value,
                    "waste_percentage": waste,
                    "efficiency_rating": rating,
                    "efficiency_color": color,
                    "message": message
                }

        except Exception as e:
            print(e)

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
        {"name": "Water", "green_rating": "⭐⭐⭐⭐⭐", "applications": "Universal solvent", "toxicity": "Non-toxic"},
        {"name": "Ethanol", "green_rating": "⭐⭐⭐⭐", "applications": "Pharma, fuel", "toxicity": "Low"},
        {"name": "Ethyl Lactate", "green_rating": "⭐⭐⭐⭐⭐", "applications": "Coatings", "toxicity": "Very Low"},
        {"name": "CO₂", "green_rating": "⭐⭐⭐⭐⭐", "applications": "Extraction", "toxicity": "Non-toxic"},
        {"name": "Acetone", "green_rating": "⭐⭐⭐", "applications": "Cleaning", "toxicity": "Moderate"},
        {"name": "Glycerol", "green_rating": "⭐⭐⭐⭐⭐", "applications": "Cosmetics", "toxicity": "Non-toxic"}
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

        flash("Submitted for review", "info")
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

@app.route('/approve/<int:id>')
@login_required
def approve_tutorial(id):
    if not current_user.is_admin():
        return redirect('/')

    tutorial = Tutorial.query.get(id)
    tutorial.approved = True

    user = User.query.filter_by(username=tutorial.user).first()
    if user:
        user.points += 20

    db.session.commit()
    return redirect(url_for('admin_tutorials'))

# ---------- LEADERBOARD ----------
@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.points.desc()).all()
    return render_template('leaderboard.html', users=users)

#####
@app.route('/chat')
def chat():
    return render_template('chatbot.html')

# ==================== RUN ====================
if __name__ == '__main__':
    app.run(debug=True)