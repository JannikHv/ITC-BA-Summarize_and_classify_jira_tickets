from transformers import GPT2LMHeadModel, GPT2Tokenizer
from ..abstract_text_summarizer import AbstractTextSummarizer

class DialoGPTSummarizer(AbstractTextSummarizer):
    def __init__(self) -> None:
        super().__init__()

        model_name = 'microsoft/DialoGPT-large'
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)

    @staticmethod
    def get_name() -> str:
        return 'DialoGPTSummarizer (microsoft/DialoGPT-large)'

    def summarize(self, input_text: str):
        task_description = 'Summarize the following text'
        prompt = f'{task_description}:\n{input_text}'
        prompt = prompt.replace('\n', '').replace('\r', '')
        input_ids = self.tokenizer.encode(prompt + self.tokenizer.eos_token, return_tensors='pt')
        generated_ids = self.model.generate(input_ids, max_length=1000, pad_token_id=self.tokenizer.eos_token_id)

        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
