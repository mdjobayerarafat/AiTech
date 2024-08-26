from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Ollama # Note: 'Ollama' should be capitalized
import csv
import requests
from bs4 import BeautifulSoup
import PyPDF2
from django.conf import settings
import os  # Add this import

# Create your views here.
# type: ignore
class ChatbotView(APIView):

    def post(self, request):
        user_message = request.data.get('message')
        
        # Initialize Ollama with Qwen2 model
        llm = Ollama(model="qwen2:1.5b")
        
        # Create a prompt template
        template = """
        You are a helpful AI assistant. Use the following information to answer the user's question:
        
        {context}
        
        User: {user_message}
        AI:
        """
        prompt = PromptTemplate(template=template, input_variables=["context", "user_message"])
        
        # Create an LLMChain
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Get context from various sources
        context = self.get_context(user_message)
        
        # Generate response
        response = chain.run(context=context, user_message=user_message)
        
        # Save the chat message
        chat_message = ChatMessage.objects.create(user_message=user_message, bot_response=response)
        serializer = ChatMessageSerializer(chat_message)
        
        return Response(serializer.data)
    
    def get_context(self, user_message):
        context = ""
        
        # Get the base directory for data files
        data_dir = os.path.join(settings.BASE_DIR, 'data')
        
        # Text file
        try:
            with open(os.path.join(data_dir, 'data.txt'), 'r') as file:
                text_data = file.read()
                context += f"Text data: {text_data}\n\n"
        except FileNotFoundError:
            context += "Text file not found.\n\n"
        
        # Website
        try:
            response = requests.get('https://example.com')
            soup = BeautifulSoup(response.text, 'html.parser')
            website_data = soup.get_text()
            context += f"Website data: {website_data}\n\n"
        except requests.RequestException:
            context += "Failed to fetch website data.\n\n"
        
        # PDF
        try:
            with open(os.path.join(data_dir, 'document.pdf'), 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                pdf_text = ""
                for page in reader.pages:
                    pdf_text += page.extract_text()
                context += f"PDF data: {pdf_text}\n\n"
        except FileNotFoundError:
            context += "PDF file not found.\n\n"
        
        # CSV
        try:
            with open(os.path.join(data_dir, 'data.csv'), 'r') as file:
                csv_reader = csv.reader(file)
                csv_data = [row for row in csv_reader]
                context += f"CSV data: {csv_data}\n\n"
        except FileNotFoundError:
            context += "CSV file not found.\n\n"
        
        return context