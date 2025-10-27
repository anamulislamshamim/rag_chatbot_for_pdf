import gradio as gr 
import requests
from dotenv import load_dotenv
import os 

load_dotenv()


API_URL = "http://localhost:8000/api/chat/"
API_KEY=os.getenv("AUTH_API_KEY")


def ask_question(question, history):
    try:
        headers = {
            "Authorization": f"Api-Key {API_KEY}",
            "Content-Type": "application/json",
        }
        data = {"question": question}
        response = requests.post(API_URL, json=data, headers=headers, timeout=60)
        if response.status_code == 200:
            return response.json().get("answer", "No answer received.")
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"⚠️ Exception: {str(e)}"
    
# Create a simple Gradio interface
iface = gr.ChatInterface(
    fn=ask_question,
    title="📄 RAG Chatbot PDF Q&A",
    description="Ask questions based on the provided PDF document. Powered by Django + Gemini + FAISS.",
    theme="soft",
    examples=[
        ["What is the company name?"],
        ["Where is it located?"],
        ["What services does it provide?"],
    ],
)

# EXPOSE THE ASGI APP
# Gradio's Blocks/Interface object has an 'app' property which is the ASGI application.
gradio_asgi_app = iface.app

if __name__ == "__main__":
    iface.launch(server_port=7860) 