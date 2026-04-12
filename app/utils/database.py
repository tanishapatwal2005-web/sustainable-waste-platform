"""
Database helper functions for Zero Waste AI Platform
"""

from datetime import datetime, date
from flask import current_app

# ==================== USER HELPERS ====================

def get_user_stats(user_id, db, models):
    """Get user statistics"""
    User = models.get('User')
    WasteRecord = models.get('WasteRecord')
    Tutorial = models.get('Tutorial')
    ChemicalReaction = models.get('ChemicalReaction')
    
    if not all([User, WasteRecord, Tutorial]):
        return None
    
    total_waste = db.session.query(db.func.sum(WasteRecord.quantity_kg)).filter_by(user_id=user_id).scalar() or 0
    total_calculations = ChemicalReaction.query.filter_by(user_id=user_id).count() if ChemicalReaction else 0
    total_contributions = Tutorial.query.filter_by(author_id=user_id, status='approved').count() if Tutorial else 0
    
    return {
        'total_waste_recycled': float(total_waste),
        'total_calculations': total_calculations,
        'total_contributions': total_contributions,
        'total_points': User.query.get(user_id).points if User else 0
    }

def get_leaderboard_data(db, User, limit=20):
    """Get leaderboard data"""
    users = User.query.filter_by(is_active=True).order_by(User.points.desc()).limit(limit).all()
    return [
        {
            'rank': idx + 1,
            'username': user.username,
            'points': user.points,
            'role': user.role
        }
        for idx, user in enumerate(users)
    ]

# ==================== WASTE HELPERS ====================

def save_waste_record(user_id, waste_type, quantity, description, db, WasteRecord):
    """Save waste classification record"""
    record = WasteRecord(
        user_id=user_id,
        waste_type=waste_type,
        quantity_kg=quantity,
        description=description,
        date_recorded=date.today()
    )
    db.session.add(record)
    db.session.commit()
    return record

def get_waste_stats(user_id, db, WasteRecord):
    """Get waste statistics for user"""
    records = WasteRecord.query.filter_by(user_id=user_id).all()
    
    stats = {}
    for record in records:
        if record.waste_type not in stats:
            stats[record.waste_type] = 0
        stats[record.waste_type] += float(record.quantity_kg)
    
    return stats

def get_waste_trends(user_id, db, WasteRecord, days=30):
    """Get waste trends for last N days"""
    from datetime import timedelta
    
    start_date = date.today() - timedelta(days=days)
    records = WasteRecord.query.filter(
        WasteRecord.user_id == user_id,
        WasteRecord.date_recorded >= start_date
    ).order_by(WasteRecord.date_recorded).all()
    
    trends = {}
    for record in records:
        date_str = record.date_recorded.strftime('%Y-%m-%d')
        if date_str not in trends:
            trends[date_str] = 0
        trends[date_str] += float(record.quantity_kg)
    
    return trends

# ==================== TUTORIAL HELPERS ====================

def get_popular_tutorials(db, Tutorial, limit=5):
    """Get most viewed tutorials"""
    return Tutorial.query.filter_by(status='approved').order_by(Tutorial.views.desc()).limit(limit).all()

def get_recent_tutorials(db, Tutorial, limit=5):
    """Get most recent tutorials"""
    return Tutorial.query.filter_by(status='approved').order_by(Tutorial.created_at.desc()).limit(limit).all()

def increment_tutorial_views(tutorial_id, db, Tutorial):
    """Increment tutorial view count"""
    tutorial = Tutorial.query.get(tutorial_id)
    if tutorial:
        tutorial.views += 1
        db.session.commit()
        return True
    return False

# ==================== ACTIVITY HELPERS ====================

def log_activity(user_id, activity_type, description, points_earned, db, UserActivity, ip_address=None):
    """Log user activity"""
    activity = UserActivity(
        user_id=user_id,
        activity_type=activity_type,
        description=description,
        points_earned=points_earned,
        ip_address=ip_address
    )
    db.session.add(activity)
    db.session.commit()
    return activity

def get_user_activities(user_id, db, UserActivity, limit=10):
    """Get user activity log"""
    return UserActivity.query.filter_by(user_id=user_id).order_by(UserActivity.created_at.desc()).limit(limit).all()

# ==================== CLEANUP HELPERS ====================

def cleanup_old_sessions(db, UserActivity, days=30):
    """Clean up old session data"""
    from datetime import timedelta
    
    cutoff_date = datetime.now() - timedelta(days=days)
    deleted = UserActivity.query.filter(UserActivity.created_at < cutoff_date).delete()
    db.session.commit()
    return deleted