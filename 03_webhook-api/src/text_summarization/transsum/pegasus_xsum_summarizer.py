from transformers import pipeline, PegasusTokenizer
from ..abstract_transsum_text_summarizer import AbstractTranssumTextSummarizer
from ...text_translation import AbstractTextTranslator
from ..transsum_text_summarization_result import TranssumTextSummarizationResult

class PegasusXSumSummarizer(AbstractTranssumTextSummarizer):
    def __init__(
        self,
        de_to_en_translator: AbstractTextTranslator,
        en_to_de_translator: AbstractTextTranslator,
    ):
        super().__init__(de_to_en_translator, en_to_de_translator)

        model_name = 'google/pegasus-xsum'
        self.tokenizer = PegasusTokenizer.from_pretrained(model_name)
        self.summarizer = pipeline(
            'summarization',
            model=model_name,
            tokenizer=self.tokenizer,
            framework='pt'
        )

    @staticmethod
    def get_name() -> str:
        return 'PegasusXSumSummarizer (google/pegasus-xsum)'

    def summarize(self, input_text: str) -> TranssumTextSummarizationResult:
        text_de = input_text
        text_en = self._pre_summarize(text_de)
        # summary_en = self.summarizer(text_en, max_length=len(input_text))[0]['summary_text'] # Not making any difference
        summary_en = self.summarizer(text_en)[0]['summary_text']
        summary_de = self._post_summarize(summary_en)

        return TranssumTextSummarizationResult(text_de, summary_de, text_en, summary_en)