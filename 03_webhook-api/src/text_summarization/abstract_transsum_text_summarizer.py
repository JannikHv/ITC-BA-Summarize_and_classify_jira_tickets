from .abstract_text_summarizer import AbstractTextSummarizer
from ..text_translation import AbstractTextTranslator
from abc import abstractmethod
from .transsum_text_summarization_result import TranssumTextSummarizationResult

class AbstractTranssumTextSummarizer(AbstractTextSummarizer):
    _de_to_en_translator: AbstractTextTranslator
    _en_to_de_translator: AbstractTextTranslator

    def __init__(
        self,
        de_to_en_translator: AbstractTextTranslator,
        en_to_de_translator: AbstractTextTranslator,
    ):
        self._de_to_en_translator = de_to_en_translator
        self._en_to_de_translator = en_to_de_translator

    def _pre_summarize(self, text_de: str) -> str:
        return self._de_to_en_translator.translate(text_de)

    def _post_summarize(self, text_en: str) -> str:
        return self._en_to_de_translator.translate(text_en)

    @abstractmethod
    def summarize(self, text: str) -> TranssumTextSummarizationResult:
        ...