from openai import ChatCompletion
from ..abstract_text_summarizer import AbstractTextSummarizer

class ChatGPTSummarizer(AbstractTextSummarizer):
    @staticmethod
    def get_name() -> str:
        return 'ChatGPTSummarizer (gpt-4)'

    def summarize(input_text: str) -> str:
        task_description = 'Fasse folgenden Text zusammen'
        prompt = f'{task_description}:\n{input_text}'
        messages = [{ 'role': 'user', 'content': prompt }]
        response = ChatCompletion.create(model='gpt-4', messages=messages, temperature=0)

        return response.choices[0].message['content']
