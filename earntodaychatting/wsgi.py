import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'earntodaychatting' project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'earntodaychatting.settings')

application = get_wsgi_application()

# Critical for Vercel deployment: Expose an 'app' alias for the serverless handler
app = application