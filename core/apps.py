from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .faiss_loader import load_index

        try:
            global faiss_index, text_chunks
            faiss_index, text_chunks = load_index()
            print("Faiss index loaded successfully.")
        except Exception as e:
            print(f"Could not load FAISS index: {e}")
