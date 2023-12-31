from abc import ABC, abstractstaticmethod, abstractmethod
from .text_summarization_result import TextSummarizationResult

class AbstractTextSummarizer(ABC):
    @abstractstaticmethod
    def get_name() -> str:
        ...

    @abstractmethod
    def summarize(self, input_text: str) -> TextSummarizationResult:
        ...