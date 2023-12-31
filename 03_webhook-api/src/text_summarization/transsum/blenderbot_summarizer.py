from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from ..abstract_transsum_text_summarizer import AbstractTranssumTextSummarizer
from ...text_translation import AbstractTextTranslator
from ..transsum_text_summarization_result import TranssumTextSummarizationResult

class BlenderbotSummarizer(AbstractTranssumTextSummarizer):
    def __init__(
        self,
        de_to_en_translator: AbstractTextTranslator,
        en_to_de_translator: AbstractTextTranslator,
    ):
        super().__init__(de_to_en_translator, en_to_de_translator)

        model_name = 'facebook/blenderbot-400M-distill'
        self.tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
        self.model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

    @staticmethod
    def get_name() -> str:
        return 'BlenderbotSummarizer (facebook/blenderbot-400M-distill)'

    def summarize(self, input_text: str) -> TranssumTextSummarizationResult:
        text_de = input_text
        text_en = self._pre_summarize(text_de)
        task_description = 'Summarize the following text'
        prompt = f'{task_description}:\n{text_en}'
        input_ids = self.tokenizer(
            prompt + self.tokenizer.eos_token,
            return_tensors='pt',
            truncation=True,
            max_length=128
        )
        generated_ids = self.model.generate(**input_ids, pad_token_id=self.tokenizer.eos_token)

        summary_en = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        summary_de = self._post_summarize(summary_en)

        return TranssumTextSummarizationResult(text_de, summary_de, text_en, summary_en)