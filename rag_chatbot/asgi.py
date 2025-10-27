import os

from django.core.asgi import get_asgi_application
# ASGI Routing Imports

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag_chatbot.settings')

# Get the standard Django ASGI app
django_asgi_app = get_asgi_application()

application = django_asgi_app