from transformers import pipeline
from ..abstract_text_summarizer import AbstractTextSummarizer
from ..text_summarization_result import TextSummarizationResult

class ML6TeamMT5Summarizer(AbstractTextSummarizer):
    def __init__(self) -> None:
        super().__init__()

        self.pipeline = pipeline('summarization', model='ml6team/mt5-small-german-finetune-mlsum')

    @staticmethod
    def get_name() -> str:
        return 'MT5Summarizer (ml6team/mt5-small-german-finetune-mlsum)'

    def summarize(self, input_text: str) -> TextSummarizationResult:
        summary = self.pipeline(input_text, max_length=len(input_text))[0]['summary_text']

        return TextSummarizationResult(input_text, summary)