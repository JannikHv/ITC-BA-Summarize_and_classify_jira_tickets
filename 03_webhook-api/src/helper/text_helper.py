from bs4 import BeautifulSoup
from html import unescape
import re

class TextHelper:
    @staticmethod
    def clean_text(text: str) -> str:
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = BeautifulSoup(unescape(text), 'lxml').text

        return text

    @staticmethod
    def count_words(text: str) -> int:
        return len(re.findall(r'\w+', text))