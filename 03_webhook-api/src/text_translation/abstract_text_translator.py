from abc import ABC, abstractmethod

class AbstractTextTranslator(ABC):
    @abstractmethod
    def translate(self, input_text: str) -> str:
        ...