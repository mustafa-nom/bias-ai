"""Simple caching to avoid re-fetching same articles."""

import json
import os
from datetime import datetime, timedelta

CACHE_FILE = "article_cache.json"
CACHE_HOURS = 24

def load_cache():
    """Load cached articles from file."""
    if not os.path.exists(CACHE_FILE):
        return {}
    
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    """Save cache to file."""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    except:
        pass

def is_cache_valid(timestamp):
    """Check if cached data is still valid."""
    try:
        cached_time = datetime.fromisoformat(timestamp)
        return datetime.now() - cached_time < timedelta(hours=CACHE_HOURS)
    except:
        return False

def get_cached_articles(topic):
    """Get cached articles for a topic."""
    cache = load_cache()
    if topic not in cache:
        return None
    
    entry = cache[topic]
    if not is_cache_valid(entry['timestamp']):
        return None
    
    return entry['articles']

def cache_articles(topic, articles):
    """Cache articles for a topic."""
    cache = load_cache()
    cache[topic] = {
        'timestamp': datetime.now().isoformat(),
        'articles': articles
    }
    save_cache(cache)