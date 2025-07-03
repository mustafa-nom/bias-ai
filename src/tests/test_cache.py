#!/usr/bin/env python3
"""Test script to verify cache.py functionality."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cache import cache_articles, get_cached_articles

# Test data
test_topic = "test_topic"
test_articles = [
    {"title": "Article 1", "url": "https://example.com/1"},
    {"title": "Article 2", "url": "https://example.com/2"}
]

print("Testing cache functionality...")

# Test caching
print("1. Caching articles...")
cache_articles(test_topic, test_articles)
print("   Articles cached successfully")

# Test retrieval
print("2. Retrieving cached articles...")
cached = get_cached_articles(test_topic)
if cached:
    print(f"   Retrieved {len(cached)} articles")
    print(f"   First article: {cached[0]['title']}")
else:
    print("   No cached articles found")

# Test non-existent topic
print("3. Testing non-existent topic...")
result = get_cached_articles("nonexistent_topic")
if result is None:
    print("   Correctly returned None for non-existent topic")
else:
    print("   Unexpected result for non-existent topic")

print("\nCache test completed!")