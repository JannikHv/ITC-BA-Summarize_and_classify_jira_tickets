from transformers import pipeline
from .abstract_spam_classifier import AbstractSpamClassifier
from .spam_classification_result import SpamClassificationResult
from ..text_translation import AbstractTextTranslator
from typing import Union

class DistilbertSpamClassifier(AbstractSpamClassifier):
    def __init__(self, de_to_en_translator: Union[AbstractTextTranslator, None] = None):
        super().__init__(de_to_en_translator)

        self.classifer = pipeline(
            'text-classification',
            model='skandavivek2/spam-classifier'
        )

    @staticmethod
    def get_name() -> str:
        return 'DistilbertSpamClassifier (skandavivek2/spam-classifier)'

    def classify(self, input_text: str) -> SpamClassificationResult:
        if self._de_to_en_translator:
            input_text = self._de_to_en_translator.translate(input_text)

        result = self.classifer(input_text, truncation=True, max_length=self.max_input_length)[0]
        spam = 1 - result['score'] if result['label'] == 'HAM' else result['score']

        return SpamClassificationResult(spam)
