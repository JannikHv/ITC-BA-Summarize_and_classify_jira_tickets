from dataclasses import dataclass
from .text_summarization_result import TextSummarizationResult

@dataclass(frozen=True)
class TranssumTextSummarizationResult(TextSummarizationResult):
    text_en: str
    summary_en: str