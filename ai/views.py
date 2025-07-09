import os
import openai
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from .bot import ask_plant_advisor
from .bot import ask_plant_advisor_with_link

openai.api_key = os.getenv("OPENAI_API_KEY")

@csrf_exempt  # For AJAX, but use CSRF token in production!
def ask_bot(request):
    if request.method == "POST":
        question = request.POST.get("question")
        if not question:
            return JsonResponse({"error": "No question provided."}, status=400)
        try:
            answer = ask_plant_advisor_with_link(question, request)
        except Exception as e:
            print("OpenAI error:", str(e))  # This will show up in your server log
            return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"answer": answer})
    return JsonResponse({"error": "POST only"}, status=405)

def ai_chat_page(request):
    return render(request, "ai_chat.html")
