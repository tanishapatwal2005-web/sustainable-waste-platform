from flask import Flask, render_template

def create_app():
    app = Flask(__name__, template_folder='templates')

    @app.route('/')
    def home():
        return render_template('sustainability_dashboard.html')

    return app