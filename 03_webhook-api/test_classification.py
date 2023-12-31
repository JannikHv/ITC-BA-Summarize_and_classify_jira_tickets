from src.spam_classification import *
from src.text_translation import *
from src.helper import *
from typing import Dict, List
import pandas as pd
import sys
import os
import random
import json

def load_spam_classifiers() -> Dict[str, AbstractSpamClassifier]:
    return {
        'bert': BertSpamClassifier(),
        'distilbert': DistilbertSpamClassifier(),
        'otis': OtisSpamClassifier(),
        'roberta': RobertaSpamClassifier()
    }

def load_samples(issues_filepath: str, sample_size: int) -> List[dict]:
    return random.sample(json.load(open(issues_filepath, 'r')), sample_size)

def print_help():
    print('Usage: python3 text_classification.py <issues.json>')

def test_classification(
    classifier_id: str,
    classifier: AbstractSpamClassifier,
    issues: List[dict],
    de_to_en_translator: AbstractTextTranslator = DeToEnTranslator(),
    en_to_de_translator: AbstractTextTranslator = EnToDeTranslator()
):
    errors: List[dict] = []
    results: List[dict] = []

    for issue in issues:
        if not issue['description']:
            errors.append({ 'issue': issue, 'message': 'Empty issue description'})
            continue

        try:
            text_de = TextHelper.clean_text(issue['description'])
            text_de_result = classifier.classify(text_de)

            text_en = de_to_en_translator.translate(text_de)
            text_en_result = classifier.classify(text_en)

            results.append({
                'text_de': text_de,
                'text_en': text_en,
                'text_de_result': text_de_result.spam,
                'text_en_result': text_en_result.spam
            })
        except Exception as e:
            errors.append({ 'issue': issue, 'message': str(e) })

    pd.DataFrame(results).to_json(f'./results-{classifier_id}.json')
    pd.DataFrame(results).to_csv(f'./results-{classifier_id}.csv')

    pd.DataFrame(errors).to_json(f'./errors-{classifier_id}.json')
    pd.DataFrame(errors).to_csv(f'./errors-{classifier_id}.csv')

spam_issues_export_filepath = sys.argv[-1]

if not os.path.isfile(spam_issues_export_filepath):
    print_help()
    quit(-1)

samples = load_samples(spam_issues_export_filepath, sample_size=10)
spam_classifiers = load_spam_classifiers()

print(f'Testing spam classification with {len(samples)} samples')

for classifier_id, classifier in spam_classifiers.items():
    test_classification(classifier_id, classifier, samples)

print('Done')