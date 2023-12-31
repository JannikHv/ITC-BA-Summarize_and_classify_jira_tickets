from transformers import pipeline
from ..abstract_text_summarizer import AbstractTextSummarizer
from ..text_summarization_result import TextSummarizationResult

class T5BaseSummarizer(AbstractTextSummarizer):
    def __init__(self) -> None:
        super().__init__()

        self.pipeline = pipeline('summarization', model='Einmalumdiewelt/T5-Base_GNAD')

    @staticmethod
    def get_name() -> str:
        return 'T5BaseSummarizer (Einmalumdiewelt/T5-Base_GNAD)'

    def summarize(self, input_text: str) -> TextSummarizationResult:
        summary = self.pipeline(input_text)[0]['summary_text']

        return TextSummarizationResult(input_text, summary)
