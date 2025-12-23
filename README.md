# Cultural Trend Aggregator

A solo-use cultural trend aggregator application built with Python and Flask that collects, analyzes, and displays trending topics from multiple sources with deeply actionable AI-powered insights.

## Features

### Data Aggregation
- **Google Trends**: Automatically fetches trending topics from Entertainment, Shopping, and Pop Culture categories
- **Reddit**: Monitors trending posts from curated subreddits (popculturechat, AskTikTok, femalefashionadvice, internetisbeautiful)
- **Manual Entries**: Add your own trend observations with custom categories and lifecycle stages

### AI-Powered Trend Analysis
Leverages OpenAI's GPT-4o model to generate comprehensive, actionable insights including:

- **Social Listening Analysis**: What people are actually saying about trends, with sentiment breakdowns showing positive reactions, criticisms, and demographic variations
- **Behavioral Economics Drivers**: Psychological motivations, cognitive biases, and decision-making factors driving trend adoption
- **Market Opportunity Identification**: Specific product gaps, service innovations, competitive advantages, and optimal timing recommendations
- **Engagement Strategies**: Concrete marketing tactics, product development ideas, community building approaches, and KPI tracking suggestions
- **Risk Assessment**: Potential backlash scenarios, regulatory considerations, competitive threats, and trend sustainability forecasts
- **Content Ideas**: Specific content angles and creative directions for capitalizing on trends

### Dashboard & Interface
- **Unified Trend View**: All trends displayed in a sortable, filterable table
- **Category Filtering**: Quick filters for Entertainment, Shopping, Pop Culture, and Social Media
- **Popularity Scoring**: Trends ranked by engagement metrics
- **Light Mode Theme**: Clean, professional interface design
- **Responsive Design**: Works on desktop and mobile devices

### Data Persistence
- **Historical Tracking**: Trend data stored in PostgreSQL for time-based analysis
- **Analysis Caching**: AI analyses cached for 12 hours to balance freshness with API efficiency
- **Trend History**: Track how trends evolve over time

## Tech Stack

- **Backend**: Python 3, Flask, SQLAlchemy
- **Database**: PostgreSQL (via Neon)
- **AI**: OpenAI GPT-4o
- **APIs**: Google Trends (pytrends), Reddit (PRAW)
- **Frontend**: Bootstrap 5, DataTables, Chart.js
- **Server**: Gunicorn

## Project Structure

```
├── app.py                 # Main Flask application with routes
├── main.py                # Application entry point
├── models.py              # SQLAlchemy database models
├── trend_analysis.py      # AI-powered trend analysis engine
├── trends_google.py       # Google Trends data fetcher
├── trends_reddit.py       # Reddit API integration
├── trends_manual.py       # Manual trend entry handler
├── templates/
│   ├── index.html         # Main dashboard template
│   ├── trend_detail.html  # Detailed trend analysis view
│   ├── manual_entry.html  # Manual trend input form
│   └── base.html          # Base template with common layout
├── static/
│   ├── css/custom.css     # Custom styling
│   └── js/main.js         # Frontend interactivity
├── data/
│   └── manual_trends.json # Storage for manual entries
└── pyproject.toml         # Python dependencies
```

## Environment Variables

The application requires the following environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `OPENAI_API_KEY` | OpenAI API key for trend analysis | Yes |
| `SESSION_SECRET` | Flask session secret key | Yes |
| `REDDIT_CLIENT_ID` | Reddit API client ID | Optional* |
| `REDDIT_CLIENT_SECRET` | Reddit API client secret | Optional* |

*Reddit credentials are optional; the app uses fallback data if not provided.

## Installation & Setup

1. **Clone the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or with uv:
   ```bash
   uv sync
   ```

3. **Set up environment variables** (see table above)

4. **Initialize the database**
   The database tables are automatically created on first run.

5. **Run the application**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reload main:app
   ```

## Usage

### Viewing Trends
1. Open the application in your browser
2. The main dashboard displays all aggregated trends in a sortable table
3. Use category filter buttons to focus on specific trend types
4. Click on any trend row to view detailed AI analysis

### Adding Manual Trends
1. Click "Add Trend" in the navigation
2. Fill in the trend details:
   - Trend name
   - Source (where you observed it)
   - Category
   - Lifecycle stage (Emerging, Growing, Peak, Declining)
   - Pop potential indicator
3. Submit to add to your trend collection

### Analyzing Trends
1. Click on any trend in the table
2. View the comprehensive AI-generated analysis with tabs for:
   - Overview & Context
   - Social Listening
   - Behavioral Drivers
   - Market Opportunities
   - Engagement Strategies
   - Risk Analysis
   - Content Ideas

## API Fallbacks

The application includes robust fallback mechanisms:
- **Google Trends**: If API rate limits are hit, uses cached/sample data
- **Reddit**: If authentication fails, uses curated sample posts
- **OpenAI**: If analysis fails, displays informative error messages

## Development

### Running in Development Mode
```bash
python main.py
```

### Database Migrations
The app uses SQLAlchemy with automatic table creation. Models are defined in `models.py`.

## License

This project is for personal/solo use.

## Contributing

This is a solo-use application. Feel free to fork and adapt for your own needs.
