from django.http import JsonResponse
import os
from django.shortcuts import render
import google.generativeai as genai

# API 키 가져오기
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")

# Google Generative AI 클라이언트 설정
genai.configure(api_key=GOOGLE_API_KEY)

model = "gemini-1.5-flash-001"


# 챗봇 페이지
def chatbot_page(request):
    return render(request, "chatbot/chatbot.html")


# AI 응답 처리
def chatbot_response(request):
    user_message = request.GET.get("message", "")

    if not user_message:
        return JsonResponse({"response": "메시지를 입력해 주세요."})

    # Google Cloud Generative AI 텍스트 생성 요청
    prompt = user_message  # 사용자가 보낸 메시지를 프롬프트로 사용

    # 텍스트 생성
    chat = genai.GenerativeModel(model).start_chat()
    response = chat.send_message(user_message)
    generated_text = response.text

    return JsonResponse({"response": generated_text})
