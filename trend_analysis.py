import os
import logging
import json
from datetime import datetime, timedelta
from openai import OpenAI  # Import OpenAI client
from models import TrendAnalysis, TrendHistory  # Import models
from app import db  # Import db from app

# Set up logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_trend(trend_name, source, category=None, details=None):
    """
    Generate deep, actionable insights for a trend using AI with social listening,
    behavioral economics drivers, and specific strategies
    
    Args:
        trend_name (str): The name of the trend
        source (str): The source of the trend (e.g., Google Trends, Reddit)
        category (str, optional): The category of the trend
        details (dict, optional): Additional details about the trend
        
    Returns:
        dict: A dictionary containing the comprehensive analysis results
    """
    try:
        # Check if we already have a recent analysis (within last 12 hours to ensure freshness)
        existing_analysis = TrendAnalysis.query.filter_by(
            trend_name=trend_name, 
            source=source
        ).filter(
            TrendAnalysis.date_analyzed > datetime.utcnow() - timedelta(hours=12)
        ).first()
        
        if existing_analysis:
            logger.info(f"Using existing analysis for {trend_name}")
            
            # Parse JSON strings if needed
            try:
                context = existing_analysis.context
                if context and (context.startswith('{') or context.startswith('[')):
                    context = json.loads(context)
                
                insights = existing_analysis.insights
                if insights and (insights.startswith('{') or insights.startswith('[')):
                    insights = json.loads(insights)
                
                implications = existing_analysis.implications
                if implications and (implications.startswith('{') or implications.startswith('[')):
                    implications = json.loads(implications)
                
                content_ideas = existing_analysis.content_ideas
                if content_ideas and (content_ideas.startswith('{') or content_ideas.startswith('[')):
                    content_ideas = json.loads(content_ideas)
                
                return {
                    "context": context,
                    "insights": insights,
                    "implications": implications,
                    "content_ideas": content_ideas
                }
            except Exception as e:
                logger.error(f"Error parsing JSON from stored analysis: {str(e)}")
                # Fall through to regenerate analysis
            
            return {
                "context": existing_analysis.context,
                "insights": existing_analysis.insights,
                "implications": existing_analysis.implications,
                "content_ideas": existing_analysis.content_ideas
            }
        
        # Create a detailed expert-level prompt for the AI with emphasis on actionable insights
        prompt = f"""
        Perform an advanced trend analysis with social listening and behavioral economics insights:
        
        Trend: {trend_name}
        Source: {source}
        {"Category: " + category if category else ""}
        
        Return comprehensive JSON with these keys:
        
        1. "social_sentiment": Detailed breakdown of what people are specifically saying about this trend:
           - Positive reactions (exact quotes and patterns)
           - Negative reactions (specific criticisms and concerns)
           - Identified demographic variations (how different age groups/regions react)
           - Intensity metrics (how strongly people feel)
        
        2. "behavioral_drivers": The specific behavioral economics factors driving this trend:
           - Core psychological motivations (status, belonging, fear, aspiration)
           - Underlying needs being addressed
           - Cognitive biases at play (scarcity, social proof, loss aversion, etc.)
           - Decision-making factors influencing adoption
        
        3. "market_opportunities": Highly specific and actionable business opportunities:
           - Exact product gaps that could be filled
           - Service innovations that align with the trend
           - Competitive advantage strategies
           - Timing recommendations with specific windows
        
        4. "engagement_strategies": Concrete action plans for different stakeholders:
           - Marketing: specific messaging, channels, and content types that will resonate
           - Product: feature priorities based on trend alignment
           - Community: how to build engaged communities around this trend
           - Metrics: specific KPIs to track success in this trend space
        
        5. "risk_analysis": Strategic risks associated with this trend:
           - Potential backlash scenarios
           - Regulatory considerations
           - Competitive threats
           - Trend sustainability forecast with timeframes
        
        Your analysis must be:
        1. Ultra-specific with ZERO generic statements
        2. Deeply actionable with exact next steps
        3. Based on factual trend patterns and behavioral economics
        4. Include specific examples of current implementations
        5. Quantify potential impact where possible (market size, growth rates)
        
        For context storage, please also include these fields from the original analysis:
        - "context": Detailed background on the trend's origin and current status
        - "content_ideas": 5 specific, high-impact content concepts with headlines and core messaging
        """
        
        # Add any additional details we have
        if details:
            prompt += f"\n\nAdditional Information:\n{json.dumps(details, indent=2)}"
        
        # Call OpenAI API for comprehensive analysis
        response = client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7,  # Balance between creativity and precision
            max_tokens=4000  # Allow for detailed comprehensive response
        )
        
        # Extract the rich, detailed result
        result = json.loads(response.choices[0].message.content)
        
        # Reshape the result to match our existing database structure while preserving new data
        reshaped_result = {
            "context": result.get("context", ""),
            "insights": result.get("social_sentiment", {}),  # Store social sentiment as insights
            "implications": {  # Combine behavioral drivers, opportunities and strategies
                "behavioral_drivers": result.get("behavioral_drivers", {}),
                "market_opportunities": result.get("market_opportunities", {}),
                "engagement_strategies": result.get("engagement_strategies", {}),
                "risk_analysis": result.get("risk_analysis", {})
            },
            "content_ideas": result.get("content_ideas", [])
        }
        
        # Store the analysis in the database
        try:
            # Convert all data to string format for database storage
            context_str = reshaped_result.get('context', '')
            if isinstance(context_str, dict) or isinstance(context_str, list):
                context_str = json.dumps(context_str)
            
            insights_str = reshaped_result.get('insights', '')
            if isinstance(insights_str, dict) or isinstance(insights_str, list):
                insights_str = json.dumps(insights_str)
            
            implications_str = reshaped_result.get('implications', '')
            if isinstance(implications_str, dict) or isinstance(implications_str, list):
                implications_str = json.dumps(implications_str)
            
            content_ideas_str = reshaped_result.get('content_ideas', '')
            if isinstance(content_ideas_str, dict) or isinstance(content_ideas_str, list):
                content_ideas_str = json.dumps(content_ideas_str)
            
            new_analysis = TrendAnalysis(
                trend_name=trend_name,
                source=source,
                context=context_str,
                insights=insights_str,
                implications=implications_str,
                content_ideas=content_ideas_str,
                date_analyzed=datetime.utcnow()
            )
            db.session.add(new_analysis)
            db.session.commit()
            
            # Log successful storage
            logger.info(f"Successfully stored enhanced analysis for {trend_name} from {source}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error storing analysis in database: {str(e)}")
        
        # Return the original comprehensive result to the frontend
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing trend {trend_name}: {str(e)}")
        return {
            "context": "Comprehensive analysis unavailable at this time.",
            "social_sentiment": "Social listening analysis unavailable.",
            "behavioral_drivers": "Behavioral economics analysis unavailable.",
            "market_opportunities": "Market opportunity analysis unavailable.",
            "engagement_strategies": "Strategic recommendations unavailable.",
            "risk_analysis": "Risk assessment unavailable.",
            "content_ideas": "Content strategy recommendations unavailable."
        }

def record_trend_data(trends):
    """
    Record trend data for historical analysis
    
    Args:
        trends (list): A list of trend dictionaries to record
    """
    try:
        for trend in trends:
            # Create a new trend history record
            trend_history = TrendHistory(
                trend_name=trend.get('trend_name'),
                source=trend.get('source'),
                category=trend.get('category'),
                popularity_score=trend.get('popularity_score', 0),
                date_recorded=datetime.utcnow()
            )
            db.session.add(trend_history)
        
        db.session.commit()
        logger.info(f"Recorded {len(trends)} trends in history")
        
    except Exception as e:
        logger.error(f"Error recording trend history: {str(e)}")
        db.session.rollback()

def get_trend_over_time(trend_name, source, time_period='week'):
    """
    Get historical data for a specific trend
    
    Args:
        trend_name (str): The name of the trend
        source (str): The source of the trend
        time_period (str): 'day', 'week', or 'month'
        
    Returns:
        list: A list of historical data points
    """
    try:
        if time_period == 'day':
            start_date = datetime.utcnow() - timedelta(days=1)
        elif time_period == 'week':
            start_date = datetime.utcnow() - timedelta(weeks=1)
        elif time_period == 'month':
            start_date = datetime.utcnow() - timedelta(days=30)
        else:
            start_date = datetime.utcnow() - timedelta(weeks=1)  # Default to week
            
        history = TrendHistory.query.filter_by(
            trend_name=trend_name,
            source=source
        ).filter(
            TrendHistory.date_recorded >= start_date
        ).order_by(
            TrendHistory.date_recorded
        ).all()
        
        # Format the data for display
        result = []
        for item in history:
            result.append({
                'date': item.date_recorded.strftime('%Y-%m-%d %H:%M'),
                'popularity_score': item.popularity_score
            })
            
        return result
        
    except Exception as e:
        logger.error(f"Error getting trend history: {str(e)}")
        return []