from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from google import genai
from core import faiss_loader
from .serializers import ChatRequestSerializers
from rest_framework.decorators import permission_classes, authentication_classes
from api_key_auth.permissions import HasAPIKey
from api_key_auth.authentication import APIKeyAuthentication


try:
    GENAI_CLIENT = genai.Client(api_key=settings.API_KEY_GEMINI)
except Exception as e:
    # Handle the error if the API key is missing or invalid on startup
    print(f"Error initializing GenAI Client: {e}")
    GENAI_CLIENT = None

class ChatView(APIView):
    # if GENAI_CLIENT:
    #     models = GENAI_CLIENT.models.list()
    #     for m in models:
    #         print(m.name)
    authentication_classes = [APIKeyAuthentication]
    # permission_classes = [HasAPIKey]
    @swagger_auto_schema(
        operation_description="Ask a question related to the PDF document.",
        request_body=ChatRequestSerializers,
        responses={
            200: openapi.Response(
                description="AI-generated answer based on the document context.",
                examples={
                    "application/json": {
                        "question": "What is the main topic of the document?",
                        "answer": "The document discusses cloud infrastructure and AI integration."
                    }
                },
            ),
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def post(self, request):
        # Ensure the client was initialized successfully
        if GENAI_CLIENT is None:
            return Response(
                {"error": "AI service is not configured. Check API key."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        serializer = ChatRequestSerializers(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data['question']
            try:
                from core.apps import faiss_index, text_chunks
                context_chunks = faiss_loader.find_similar_chunks(question, faiss_index, text_chunks)
                context = "\n".join(context_chunks)

                prompt = f"Use the context below to answer:\n\n{context}\n\nQuestion: {question}"
                ai_response = GENAI_CLIENT.models.generate_content(
                    model='models/gemini-2.5-flash',  # Use the canonical model name
                    contents=prompt
                )

                return Response({
                    "question": question,
                    "answer": ai_response.text
                })
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
