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
    prompt = f"""
            유저와 당신은 친구이며, 당신은 유저에게 도움이 되는 존재입니다다. 유저 메시지: {user_message}
            아래의 지시사항에 따라 응답하세요:
            1. 부정적인 답변은 피하세요. 긍정적이고 상대에게 힘을 복돋아 주는 대답을 하세요.
            2. 질문에 대한 정확하고 명확한 답을 주세요.
            3. 친절하고 도움이 되는 톤으로 대답해 주세요. 말끝마다 이모지를 붙이고, 친근한 20대 초반 여성의 말투로 대화해 주세요.
            4. 무조건 반말을 사용해 주세요.
            """  # 사용자가 보낸 메시지를 프롬프트로 사용

    # 텍스트 생성
    chat = genai.GenerativeModel(model).start_chat()
    response = chat.send_message(user_message)
    generated_text = response.text

    return JsonResponse({"response": generated_text})
