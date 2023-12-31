from transformers import pipeline
from ..abstract_text_summarizer import AbstractTextSummarizer
from ..text_summarization_result import TextSummarizationResult

class TSystemsMT5Summarizer(AbstractTextSummarizer):
    def __init__(self) -> None:
        super().__init__()

        self.pipeline = pipeline('summarization', model='T-Systems-onsite/mt5-small-sum-de-en-v2')

    @staticmethod
    def get_name() -> str:
        return 'TSystemsMT5Summarizer (T-Systems-onsite/mt5-small-sum-de-en-v2)'

    def summarize(self, input_text: str) -> TextSummarizationResult:
        summary = self.pipeline(input_text, truncation=True, max_length=len(input_text))[0]['summary_text']

        return TextSummarizationResult(input_text, summary)