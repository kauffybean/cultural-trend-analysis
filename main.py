from app import app, db  # noqa: F401

# Create database tables if they don't exist
with app.app_context():
    from models import TrendHistory, TrendAnalysis
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
