from transformers import pipeline
from ..abstract_transsum_text_summarizer import AbstractTranssumTextSummarizer
from ...text_translation import AbstractTextTranslator
from ..transsum_text_summarization_result import TranssumTextSummarizationResult

class DistilbartSummarizer(AbstractTranssumTextSummarizer):
    def __init__(
        self,
        de_to_en_translator: AbstractTextTranslator,
        en_to_de_translator: AbstractTextTranslator,
    ):
        super().__init__(de_to_en_translator, en_to_de_translator)

        self.summarizer = pipeline(
            'summarization',
            model='sshleifer/distilbart-cnn-12-6',
            truncation=True
        )

    @staticmethod
    def get_name() -> str:
        return 'DistilbartSummarizer (sshleifer/distilbart-cnn-12-6)'

    def summarize(self, input_text: str) -> TranssumTextSummarizationResult:
        text_de = input_text
        text_en = self._pre_summarize(text_de)
        summary_en = self.summarizer(text_en)[0]['summary_text']
        summary_de = self._post_summarize(summary_en)

        return TranssumTextSummarizationResult(text_de, summary_de, text_en, summary_en)