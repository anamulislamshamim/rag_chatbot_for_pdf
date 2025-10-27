import os

from django.core.asgi import get_asgi_application
# ASGI Routing Imports
from starlette.routing import Mount
from starlette.applications import Starlette

# import Gradio ASGI app object
from .gradio_app import gradio_asgi_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag_chatbot.settings')

# Get the standard Django ASGI app
django_asgi_app = get_asgi_application()

# Combine the both ASGI app
# # This Starlette application will route requests to 
# either Django or Gradio based on the URL path.
application = Starlette(
    routes=[
        # Mount the Gradio application at the desired path. 
        # For a main feature, a path like "/chatbot" or 
        # even the root path is common.
        Mount("/rag_chatbot", app=gradio_asgi_app),
        # Mount the Django application for everything 
        # else (admin, other views, etc.)
        Mount("/", app=django_asgi_app),
    ]
)
