from src.helper import TextHelper
from src.text_translation import DeToEnTranslator, EnToDeTranslator
from tqe import TQE

import pandas as pd
import json
import sys
import os

def print_help():
    print('Usage: python3 test_translation.py <issues_export.json>')

issues_export_filepath = sys.argv[-1]

if not os.path.isfile(issues_export_filepath):
    print_help()
    quit(-1)

issues = json.load(open(issues_export_filepath, 'r'))
results = []
errors = []
quality_estimator_model = TQE('LaBSE')
de_to_en_translator = DeToEnTranslator()
en_to_de_translator = EnToDeTranslator()

for index, issue in enumerate(issues):
    print(f'Issue {index + 1} of {len(issues)}')

    if not issue['description']:
        print(f'Empty description, skipping')
        continue

    text_de = None
    text_en = None
    quality = None

    try:
        text_de = TextHelper.clean_text(issue['description'])
        text_en = de_to_en_translator.translate(text_de)
        quality = quality_estimator_model.fit([text_de], [text_en])[0]

        results.append({
            'text_de': text_de,
            'text_en': text_en,
            'quality': quality
        })
    except IndexError as e:
        errors.append({
            'issue': issue,
            'text_de': text_de,
            'text_en': text_en,
            'quality': quality,
            'reason': 'DE to EN translation and TQE'
        })

    if text_de and text_en:
        try:
            text_de = en_to_de_translator.translate(text_en)
            quality = quality_estimator_model.fit([text_de], [text_en])[0]

            results.append({
                'text_de': text_de,
                'text_en': text_en,
                'quality': quality
            })
        except IndexError as e:
            errors.append({
                'issue': issue,
                'text_de': text_de,
                'text_en': text_en,
                'quality': quality,
                'reason': 'EN to DE translation and TQE'
            })

pd.DataFrame(results).to_csv('translation-results.csv')
pd.DataFrame(results).to_json('translation-results.json')

pd.DataFrame(errors).to_csv('translation-errors.csv')
pd.DataFrame(errors).to_json('translation-errors.json')

# Print results
qualities = [item['quality'] for item in results]
quality_avg = sum(qualities) / len(qualities)
print(f'Found {len(errors)} errors')
print(f'Average translation quality = ~{round(quality_avg * 100, 2)}% based on {len(results)} out of {len(issues)} results')