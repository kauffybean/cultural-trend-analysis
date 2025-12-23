# Cultural Trend Aggregator

## Overview

A solo-use cultural trend aggregator application that collects, analyzes, and displays trending topics from multiple sources (Google Trends, Reddit, manual entries) with AI-powered insights. The application provides a unified dashboard for tracking cultural trends across entertainment, shopping, pop culture, and social media categories, featuring GPT-4o-generated analysis including social listening, behavioral economics drivers, market opportunities, and engagement strategies.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask** serves as the web framework, handling routing, templates, and API endpoints
- **SQLAlchemy** with a custom `DeclarativeBase` provides ORM functionality for database operations
- **Gunicorn** is used as the production WSGI server

### Data Layer
- **PostgreSQL** (via Neon) stores persistent data including trend history and AI analyses
- **JSON file storage** (`data/` directory) handles manual trends and trend caching
- **15-minute cache system** prevents excessive API calls on page loads by storing aggregated trends temporarily

### Data Models
- `TrendHistory`: Tracks trend data over time (name, source, category, popularity score, timestamp)
- `TrendAnalysis`: Stores AI-generated insights (context, insights, implications, content ideas) with 12-hour cache validity

### Trend Sources
1. **Google Trends** (`trends_google.py`): Uses `pytrends` library to fetch trending topics from Entertainment, Shopping, and Pop Culture categories
2. **Reddit** (`trends_reddit.py`): Uses `praw` library to monitor curated subreddits with fallback data when API fails
3. **Manual Entry** (`trends_manual.py`): JSON-based storage for user-submitted trend observations

### AI Analysis Engine
- `trend_analysis.py` interfaces with OpenAI's GPT-4o model
- Generates comprehensive insights including social listening, behavioral economics, market opportunities, risk assessment, and content ideas
- Implements 12-hour caching to balance freshness with API cost efficiency

### Frontend
- **Bootstrap 5** provides responsive UI components
- **DataTables** enables sortable, filterable trend tables
- **Jinja2 templates** render dynamic content with a consistent layout
- Light mode theme with custom CSS styling

### Deployment Architecture
- **Health Check**: `/health` endpoint responds in <5ms for deployment probes
- **Trend Caching**: `trend_cache.py` stores fetched trends in JSON for 15-minute intervals
- **Lazy Loading**: Index page loads from cache only; use `/fetch-trends` to refresh data
- **Refresh Button**: UI provides manual "Refresh Trends" button to trigger data fetching

### Application Entry Points
- `main.py`: Primary entry point, initializes database tables and runs Flask app
- `app.py`: Core Flask application with routes and configuration
- Multiple demo/test files exist for development purposes (`demo_app.py`, `simple_run.py`, etc.)

## External Dependencies

### APIs & Services
- **OpenAI API** (GPT-4o): Requires `OPENAI_API_KEY` environment variable for trend analysis
- **Reddit API**: Requires `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` for fetching subreddit trends; falls back to sample data if unavailable
- **Google Trends**: Uses `pytrends` library (unofficial API wrapper, no credentials required)

### Database
- **PostgreSQL**: Configured via `DATABASE_URL` environment variable, uses connection pooling with 300-second recycle and pre-ping enabled

### Key Python Packages
- `flask` and `flask-sqlalchemy`: Web framework and ORM
- `openai`: AI analysis integration
- `praw`: Reddit API wrapper
- `pytrends`: Google Trends data fetching
- `gunicorn`: Production server

### Environment Variables Required
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API authentication
- `REDDIT_CLIENT_ID`: Reddit API client ID
- `REDDIT_CLIENT_SECRET`: Reddit API client secret
- `SESSION_SECRET`: Flask session encryption key (optional, has default)