from dataclasses import dataclass

@dataclass(frozen=True)
class TextSummarizationResult:
    text_de: str
    summary_de: str