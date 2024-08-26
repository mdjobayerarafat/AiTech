import csv
import requests
from bs4 import BeautifulSoup
import PyPDF2

def get_context(self, user_message):
    context = ""
    
    # Text file
    with open('data.txt', 'r') as file:
        text_data = file.read()
        context += f"Text data: {text_data}\n\n"
    
    # Website
    response = requests.get('https://example.com')
    soup = BeautifulSoup(response.text, 'html.parser')
    website_data = soup.get_text()
    context += f"Website data: {website_data}\n\n"
    
    # PDF
    with open('document.pdf', 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()
        context += f"PDF data: {pdf_text}\n\n"
    
    # CSV
    with open('data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        csv_data = [row for row in csv_reader]
        context += f"CSV data: {csv_data}\n\n"
    
    return context