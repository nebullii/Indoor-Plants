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
    # First, replace markdown links as before
    markdown_link_pattern = re.compile(r'\[(.*?)\]\(PRODUCT_LINK\)')
    matches = markdown_link_pattern.findall(answer)
    already_linked = set()
    for plant_name in matches:
        try:
            product = Product.objects.get(name__iexact=plant_name)
            url = request.build_absolute_uri(reverse('products:product_detail', args=[product.slug]))
            answer = re.sub(rf'\[{re.escape(plant_name)}\]\(PRODUCT_LINK\)', f"<a href='{url}' target='_blank'>{plant_name}</a>", answer, count=1)
            already_linked.add(plant_name.lower())
        except Product.DoesNotExist:
            answer = re.sub(rf'\[{re.escape(plant_name)}\]\(PRODUCT_LINK\)', plant_name, answer, count=1)
    # Then, linkify any plain plant names not already linked
    for product in Product.objects.all():
        pname = product.name
        if pname.lower() in already_linked:
            continue
        url = request.build_absolute_uri(reverse('products:product_detail', args=[product.slug]))
        # Only replace if not already inside an <a> tag
        pattern = re.compile(rf'(?<![>\w])({re.escape(pname)})(?![^<]*?>)', re.IGNORECASE)
        answer = pattern.sub(f"<a href='{url}' target='_blank'>{pname}</a>", answer, count=1)
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
            url = reverse('products:product_detail', args=[product.slug])
            links.append((url, product.name))
    return links 