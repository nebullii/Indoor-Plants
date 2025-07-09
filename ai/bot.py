import os
import openai
from products.models import Product
from django.urls import reverse

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

def find_plant_link(question):
    # Simple approach: check if any product name is in the question
    for product in Product.objects.all():
        if product.name.lower() in question.lower():
            # Build the product detail URL
            url = reverse('products:product_detail', args=[product.id])
            return url, product.name
    return None, None

def ask_plant_advisor_with_link(question, request):
    answer = ask_plant_advisor(question)
    url, plant_name = find_plant_link(question)
    if url:
        full_url = request.build_absolute_uri(url)
        answer += f"\n\nView {plant_name} in our marketplace: {full_url}"
    return answer 