from django.core.wsgi import get_wsgi_application
import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neu_cse.settings')
django.setup()

from cse_app.models import TechNews
from django.utils import timezone

# Check if we have any tech news
tech_news_count = TechNews.objects.count()
print(f"Current number of tech news items: {tech_news_count}")

# Add sample tech news if none exist
if tech_news_count == 0:
    sample_news = [
        {
            'title': 'AI Breakthrough in Computer Vision',
            'content': 'Researchers have developed a new AI model that can understand complex visual scenes with unprecedented accuracy. This breakthrough could have significant implications for autonomous vehicles and medical imaging.',
            'source': 'Tech Research Monthly',
            'published_date': timezone.now()
        },
        {
            'title': 'Quantum Computing Milestone Achieved',
            'content': 'Scientists have successfully demonstrated quantum supremacy in a new experiment, solving a complex problem in minutes that would take classical computers thousands of years.',
            'source': 'Science Daily',
            'published_date': timezone.now()
        },
        {
            'title': 'New Programming Language for AI Development',
            'content': 'A new programming language specifically designed for AI development has been released. The language promises to make AI development more accessible and efficient.',
            'source': 'Developer Weekly',
            'published_date': timezone.now()
        }
    ]
    
    for news in sample_news:
        TechNews.objects.create(**news)
    print("Added sample tech news items!")