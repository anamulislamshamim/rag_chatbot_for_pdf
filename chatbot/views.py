from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import google.generativeai as genai 
from core import faiss_loader
from .serializers import ChatRequestSerializers


genai.configure(api_key=settings.API_KEY_GEMINI)

class ChatView(APIView):
    def post(self, request):
        serializer = ChatRequestSerializers(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data['question']
            try:
                from core.apps import faiss_index, text_chunks
                context_chunks = faiss_loader.find_similar_chunks(question, faiss_index, text_chunks)
                context = "\n".join(context_chunks)

                model = genai.GenerativeModel('gemini-pro')
                prompt = f"Use the context below to answer:\n\n{context}\n\nQuestion: {question}"
                ai_response = model.generate_content(prompt)

                return Response({
                    "question": question,
                    "answer": ai_response.text
                })
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
