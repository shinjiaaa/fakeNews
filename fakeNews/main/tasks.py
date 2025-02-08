from celery import shared_task
from transformers import pipeline

generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')

@shared_task(bind=True)
def generate_fake_news(self):
    try:
        prompt = "Generate a fake news headline about a breakthrough in technology."
        generated_news = generator(prompt, max_length=100, num_return_sequences=1, truncation=True)
        return generated_news[0]['generated_text']
    except Exception as e:
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        return str(e)
