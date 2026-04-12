"""
Helper functions for Zero Waste AI Platform
"""

import os
import re
import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import flash, redirect, url_for, current_app, session

# ==================== STRING HELPERS ====================

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Escape special characters
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return text.strip()

def truncate_text(text, max_length=100):
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

# ==================== DATE HELPERS ====================

def format_date(date_obj, format_str="%B %d, %Y"):
    """Format date object to string"""
    if not date_obj:
        return ""
    return date_obj.strftime(format_str)

def get_date_range(days=30):
    """Get date range for last N days"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def get_week_dates():
    """Get current week date range"""
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

# ==================== POINTS & GAMIFICATION ====================

POINTS_CONFIG = {
    'waste_classification': 10,
    'atom_economy': 15,
    'reaction_optimizer': 15,
    'green_solvent_search': 5,
    'tutorial_submit': 50,
    'tutorial_approved': 50,
    'share_result': 5,
    'daily_login': 10,
    'referral': 100,
}

def calculate_points(action, quantity=None):
    """Calculate points for an action"""
    base_points = POINTS_CONFIG.get(action, 0)
    
    # Bonus points for quantity
    if quantity and action == 'waste_classification':
        base_points += int(quantity) * 2
    
    return base_points

def check_badge_earned(user_points, waste_recycled, tutorials_approved):
    """Check which badges a user has earned"""
    badges = []
    
    if waste_recycled >= 100:
        badges.append('Recycler')
    if waste_recycled >= 500:
        badges.append('Master Recycler')
    
    if user_points >= 100:
        badges.append('Green Starter')
    if user_points >= 500:
        badges.append('Eco Warrior')
    if user_points >= 1000:
        badges.append('Zero Waste Hero')
    
    if tutorials_approved >= 1:
        badges.append('Contributor')
    if tutorials_approved >= 5:
        badges.append('Master Contributor')
    
    return badges

# ==================== VALIDATION HELPERS ====================

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Strong password"

def get_password_strength(password):
    """Get password strength score (0-100)"""
    score = 0
    if len(password) >= 6:
        score += 20
    if len(password) >= 10:
        score += 20
    if re.search(r'[a-z]', password):
        score += 15
    if re.search(r'[A-Z]', password):
        score += 15
    if re.search(r'[0-9]', password):
        score += 15
    if re.search(r'[@$!%*#?&]', password):
        score += 15
    return min(score, 100)

# ==================== FILE HELPERS ====================

def allowed_file(filename, allowed_extensions=None):
    """Check if file extension is allowed"""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_size(filepath):
    """Get file size in human readable format"""
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def generate_unique_filename(original_filename):
    """Generate unique filename"""
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    random_string = secrets.token_hex(4)
    return f"{name}_{timestamp}_{random_string}{ext}"

# ==================== ENVIRONMENT HELPERS ====================

def is_development():
    """Check if running in development mode"""
    return os.environ.get('FLASK_ENV', 'development') == 'development'

def get_app_version():
    """Get application version"""
    return "1.0.0"

# ==================== CACHE HELPERS ====================

class SimpleCache:
    """Simple in-memory cache"""
    
    def __init__(self):
        self.cache = {}
    
    def set(self, key, value, timeout=300):
        """Set cache value with timeout in seconds"""
        self.cache[key] = {
            'value': value,
            'expires': datetime.now().timestamp() + timeout
        }
    
    def get(self, key):
        """Get cache value if not expired"""
        if key in self.cache:
            item = self.cache[key]
            if datetime.now().timestamp() < item['expires']:
                return item['value']
            else:
                del self.cache[key]
        return None
    
    def delete(self, key):
        """Delete cache key"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()

# ==================== RESPONSE HELPERS ====================

def json_response(success=True, message="", data=None, status=200):
    """Create JSON response"""
    from flask import jsonify
    response = {
        'success': success,
        'message': message,
        'data': data
    }
    return jsonify(response), status

# ==================== WASTE CALCULATIONS ====================

def calculate_carbon_savings(weight_kg, waste_type):
    """Calculate carbon savings from recycling"""
    carbon_factors = {
        'Plastic': 1.5,
        'Paper': 1.0,
        'Glass': 0.5,
        'Metal': 2.0,
        'Organic': 0.3,
        'E-Waste': 2.5
    }
    factor = carbon_factors.get(waste_type, 1.0)
    return weight_kg * factor

def calculate_energy_savings(weight_kg, waste_type):
    """Calculate energy savings in kWh"""
    energy_factors = {
        'Plastic': 5.0,
        'Paper': 4.0,
        'Glass': 1.5,
        'Metal': 8.0,
        'Organic': 0.5,
        'E-Waste': 10.0
    }
    factor = energy_factors.get(waste_type, 2.0)
    return weight_kg * factor

def calculate_water_savings(weight_kg, waste_type):
    """Calculate water savings in liters"""
    water_factors = {
        'Plastic': 100,
        'Paper': 50,
        'Glass': 30,
        'Metal': 150,
        'Organic': 20,
        'E-Waste': 200
    }
    factor = water_factors.get(waste_type, 50)
    return weight_kg * factor

# ==================== GREEN CHEMISTRY HELPERS ====================

def calculate_atom_economy(reactants_weight, products_weight):
    """Calculate atom economy percentage"""
    if reactants_weight <= 0:
        return 0
    return (products_weight / reactants_weight) * 100

def get_efficiency_rating(atom_economy):
    """Get efficiency rating based on atom economy"""
    if atom_economy >= 90:
        return {'rating': 'Excellent', 'color': 'success', 'icon': 'trophy'}
    elif atom_economy >= 70:
        return {'rating': 'Good', 'color': 'info', 'icon': 'check-circle'}
    elif atom_economy >= 50:
        return {'rating': 'Average', 'color': 'warning', 'icon': 'exclamation-triangle'}
    else:
        return {'rating': 'Poor', 'color': 'danger', 'icon': 'times-circle'}

# ==================== NOTIFICATION HELPERS ====================

def flash_errors(form):
    """Flash form validation errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{field}: {error}", 'danger')

def flash_success(message):
    """Flash success message"""
    flash(message, 'success')

def flash_error(message):
    """Flash error message"""
    flash(message, 'danger')

def flash_warning(message):
    """Flash warning message"""
    flash(message, 'warning')

# ==================== SESSION HELPERS ====================

def set_session_data(key, value):
    """Set session data"""
    session[key] = value

def get_session_data(key, default=None):
    """Get session data"""
    return session.get(key, default)

def clear_session_data(key=None):
    """Clear session data"""
    if key:
        session.pop(key, None)
    else:
        session.clear()

# ==================== ANALYTICS HELPERS ====================

def calculate_recycling_rate(total_waste, recycled_waste):
    """Calculate recycling rate percentage"""
    if total_waste <= 0:
        return 0
    return (recycled_waste / total_waste) * 100

def get_environmental_impact(total_waste_recycled):
    """Calculate overall environmental impact"""
    return {
        'co2_saved': total_waste_recycled * 0.5,
        'trees_saved': total_waste_recycled / 25,
        'energy_saved': total_waste_recycled * 4,
        'water_saved': total_waste_recycled * 50
    }