from transformers import pipeline
from celery import shared_task

# Hugging Face 모델 불러오기
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')

@shared_task
def generate_fake_news():
    prompt = "Generate a fake news headline about a breakthrough in technology."
    generated_news = generator(prompt, max_length=100, num_return_sequences=1)
    return generated_news[0]['generated_text']
