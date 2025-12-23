from datetime import datetime
from app import db  # Import db from app

class TrendHistory(db.Model):
    """Model for storing trend history data for time-based analysis"""
    id = db.Column(db.Integer, primary_key=True)
    trend_name = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    popularity_score = db.Column(db.Float, default=0)
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TrendHistory {self.trend_name} from {self.source} on {self.date_recorded}>'

class TrendAnalysis(db.Model):
    """Model for storing AI-generated trend analysis"""
    id = db.Column(db.Integer, primary_key=True)
    trend_name = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    context = db.Column(db.Text)  # Contextual information about the trend
    insights = db.Column(db.Text)  # Key insights about the trend
    implications = db.Column(db.Text)  # What the trend might mean for various industries
    content_ideas = db.Column(db.Text)  # Content ideas related to the trend
    date_analyzed = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TrendAnalysis {self.trend_name}>'