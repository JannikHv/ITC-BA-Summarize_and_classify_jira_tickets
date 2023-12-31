from .abstract_text_translator import AbstractTextTranslator
from transformers import MarianMTModel, AutoTokenizer

class EnToDeTranslator(AbstractTextTranslator):
    def __init__(self) -> None:
        super().__init__()

        model_name = 'Helsinki-NLP/opus-mt-en-de'
        self.__model = MarianMTModel.from_pretrained(model_name)
        self.__tokenizer = AutoTokenizer.from_pretrained(model_name)

    def translate(self, input_text: str) -> str:
        input_ids = self.__tokenizer(input_text, return_tensors='pt')
        generated_ids = self.__model.generate(**input_ids)

        return self.__tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
