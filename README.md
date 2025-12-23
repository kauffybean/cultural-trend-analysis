# Cultural Trend Aggregator

A solo-use cultural trend aggregator built with Python and Flask that collects, analyzes, and synthesizes emerging cultural signals into deeply actionable, AI-powered insights.

This tool is designed to reduce the friction between *observing trends* and *turning them into decisions*—whether that’s content strategy, affiliate monetization, or early product exploration.

---

## Why I Built This

I started this project after recognizing a consistent gap between how trends are *discussed* and how they are actually *monetized*.

From an affiliate marketing and content strategy perspective, there is real leverage in understanding:
- What people are searching for
- How interest evolves over time (long-tail, seasonal, brand-driven)
- Where cultural curiosity turns into purchase intent

I sketched out a simple three-phase path to monetization:
1. **Trend discovery & pattern recognition**
2. Strategic content creation aligned to intent
3. Monetization through affiliate, brand, or product channels

This application is intentionally focused on **Phase 1: research**.

Before building this, my options were:
- Scraping data ad hoc with R or Python scripts (powerful, but clunky and slow for daily use)
- Paying for expensive keyword and trend tools that optimize for SEO volume, not cultural context
- Manually stitching together insights across Google Trends, Reddit, and social platforms—high effort, low signal

What frustrated me most wasn’t the lack of data—it was the *cost and friction required to get to a real insight*.

I wanted a tool that:
- Aggregates cultural signals in one place
- Surfaces *why* something is trending, not just that it is
- Translates raw signals into actionable thinking: risks, opportunities, and strategic angles

This is very much a **version 1**—a side project built to scratch a personal itch—but it reflects how I think about product design, research tooling, and monetization pathways. It’s opinionated, lightweight, and intentionally focused on clarity over exhaustiveness.

---

## Features

### Data Aggregation
- **Google Trends**: Automatically fetches trending topics from Entertainment, Shopping, and Pop Culture categories
- **Reddit**: Monitors trending posts from curated subreddits (popculturechat, AskTikTok, femalefashionadvice, internetisbeautiful)
- **Manual Entries**: Add first-hand trend observations with custom categories and lifecycle stages

### AI-Powered Trend Analysis
Leverages OpenAI’s GPT-4o model to generate structured, decision-oriented insights:

- **Social Listening Analysis**: What people are actually saying, with sentiment breakdowns and points of tension
- **Behavioral Economics Drivers**: Psychological motivations and adoption mechanics
- **Market Opportunity Identification**: Product gaps, timing considerations, and monetization angles
- **Engagement Strategies**: Content ideas, community hooks, and execution suggestions
- **Risk Assessment**: Sustainability, backlash, and competitive saturation
- **Content Ideation**: Specific creative directions informed by cultural context

### Dashboard & Interface
- **Unified Trend View**: All trends in a sortable, filterable table
- **Category Filtering**: Entertainment, Shopping, Pop Culture, Social Media
- **Popularity Scoring**: Lightweight ranking based on engagement signals
- **Clean UI**: Light mode, responsive, and designed for frequent use

### Data Persistence
- **Historical Tracking**: PostgreSQL-backed trend storage for time-based analysis
- **Analysis Caching**: AI insights cached for efficiency without sacrificing freshness
- **Trend Evolution**: Observe how interest changes across lifecycle stages
