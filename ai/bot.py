import os
import openai
from products.models import Product
from django.urls import reverse
import re

PROMPT_PATH = os.path.join(os.path.dirname(__file__), 'prompts', 'plant_qa.txt')

# Load the system prompt template
with open(PROMPT_PATH, 'r') as f:
    SYSTEM_PROMPT = f.read().strip()

openai.api_key = os.getenv('OPENAI_API_KEY')

def ask_plant_advisor(question):
    """
    Sends a plant-related question to the OpenAI API and returns the answer.
    """
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]   
    )
    answer = response.choices[0].message.content.strip()
    return answer

def ask_plant_advisor_with_links(question, request):
    answer = ask_plant_advisor(question)
    combined_text = question + " " + answer
    links = find_plant_links(combined_text)
    # Replace plant names in the answer with links
    for url, name in links:
        full_url = request.build_absolute_uri(url)
        # Use regex to replace only the first occurrence, case-insensitive
        pattern = re.compile(re.escape(name), re.IGNORECASE)
        answer = pattern.sub(
            f"<a href='{full_url}' target='_blank'>{name}</a>", answer, count=1
        )
    return answer

def find_plant_links(text):
    links = []
    text = text.lower()
    # Remove punctuation for better matching
    text = re.sub(r'[^\w\s]', '', text)
    for product in Product.objects.all():
        product_name = product.name.lower()
        product_name_clean = re.sub(r'[^\w\s]', '', product_name)
        if product_name in text or product_name_clean in text:
            url = reverse('products:product_detail', args=[product.id])
            links.append((url, product.name))
    return links 