from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from langchain import LLMChain, PromptTemplate
from langchain.llms import ollama

# Create your views here.
class ChatbotView(APIView):
    def post(self, request):
        user_message = request.data.get('message')
        
        # Initialize Ollama with Qwen2 model
        llm = Ollama(model="qwen2")
        
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
        
        # Get context from various sources (implement this function)
        context = self.get_context(user_message)
        
        # Generate response
        response = chain.run(context=context, user_message=user_message)
        
        # Save the chat message
        chat_message = ChatMessage.objects.create(user_message=user_message, bot_response=response)
        serializer = ChatMessageSerializer(chat_message)
        
        return Response(serializer.data)
    
    def get_context(self, user_message):
        # Implement logic to retrieve relevant information from text, website, PDF, and CSV
        # This is a placeholder function
        return "Relevant context from various sources"