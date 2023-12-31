from abc import ABC, abstractstaticmethod, abstractmethod, abstractproperty
from .spam_classification_result import SpamClassificationResult
from ..text_translation import AbstractTextTranslator
from typing import Union

class AbstractSpamClassifier(ABC):
    _de_to_en_translator: Union[AbstractTextTranslator, None]

    def __init__(self, de_to_en_translator: Union[AbstractTextTranslator, None] = None):
        self._de_to_en_translator = de_to_en_translator

    @abstractstaticmethod
    def get_name() -> str:
        ...

    @abstractmethod
    def classify(self, input_text: str) -> SpamClassificationResult:
        ...

    @property
    def max_input_length(self) -> int: self.classifer.tokenizer.model_max_length