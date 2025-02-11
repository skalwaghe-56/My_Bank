# app.py

from flask import Flask, render_template
from datetime import datetime
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)

# IMPORTANT: Replace 'your-production-secret-key' with a secure, unpredictable value in production.
app.config['SECRET_KEY'] = 'your-production-secret-key'

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

# Inject current year into all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}

# Main route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # For development, you can use app.run(). In production, use a WSGI server like Gunicorn.
    app.run(debug=True)