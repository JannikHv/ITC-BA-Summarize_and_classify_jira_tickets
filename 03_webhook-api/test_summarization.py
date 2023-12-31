from typing import List, Dict
from src.text_summarization import *
from src.text_translation import *
from src.helper import *
import pandas as pd
import random
import json
import sys
import os

def load_transsum_summarizers() -> Dict[str, AbstractTranssumTextSummarizer]:
    de_to_en_translator = DeToEnTranslator()
    en_to_de_translator = EnToDeTranslator()

    return {
        'distilbart': DistilbartSummarizer(de_to_en_translator, en_to_de_translator),
        'flan_t5': FlanT5Summarizer(de_to_en_translator, en_to_de_translator),
        'bart_facebook': BartFacebookSummarizer(de_to_en_translator, en_to_de_translator),
        'bart_custom': BartCustomSummarizer(de_to_en_translator, en_to_de_translator),
        'pegasus_xsum': PegasusXSumSummarizer(de_to_en_translator, en_to_de_translator),
        'pegasus_samsum': PegasusSamsumSummarizer(de_to_en_translator, en_to_de_translator)
    }

def load_de_summarizers() -> Dict[str, AbstractTextSummarizer]:
    return {
        'ml6team_mt5': ML6TeamMT5Summarizer(),
        't_systems_mt5': TSystemsMT5Summarizer(),
        't5_base': T5BaseSummarizer()
    }

def load_samples(issues_filepath: str, sample_size: int) -> List[dict]:
    issues = json.load(open(issues_filepath, 'r'))

    return random.sample(issues, sample_size)

def print_help():
    print('Usage: python3 test_summarization.py <issues.json>')

def test_summarizer(
    summarizer_id: str,
    summarizer: AbstractTextSummarizer,
    issues: List[dict]
):
    errors: List[dict] = []
    results: List[dict] = []

    for issue in issues:
        if not issue['description']:
            errors.append({ 'issue': issue, 'message': 'Empty issue description'})
            continue

        try:
            text = TextHelper.clean_text(issue['description'])
            result = summarizer.summarize(text)

            if isinstance(result, TranssumTextSummarizationResult):
                results.append({
                    'text_de': result.text_de,
                    'text_en': result.text_en,
                    'summary_en': result.summary_en,
                    'summary_de': result.summary_de
                })
            else:
                result = summarizer.summarize(text)

                results.append({
                    'text_de': result.text_de,
                    'text_en': None,
                    'summary_en': None,
                    'summary_de': result.summary_de
                })

        except Exception as e:
            results.append({ 'text_de': None, 'text_en': None, 'summary_en': None, 'summary_de': None })
            errors.append({ 'issue': issue, 'message': str(e) })

    pd.DataFrame(results).to_json(f'./results-{summarizer_id}.json')
    pd.DataFrame(results).to_csv(f'./results-{summarizer_id}.csv')

    pd.DataFrame(errors).to_json(f'./errors-{summarizer_id}.json')
    pd.DataFrame(errors).to_csv(f'./errors-{summarizer_id}.csv')

issues_export_filepath = sys.argv[-1]

if not os.path.isfile(issues_export_filepath):
    print_help()
    quit(-1)

samples = load_samples(issues_export_filepath, sample_size=50)

print(f'Testing summaries with {len(samples)} samples')

for summarizer_id, summarizer in load_transsum_summarizers().items():
    test_summarizer(summarizer_id, summarizer, samples)

for summarizer_id, summarizer in load_de_summarizers().items():
    test_summarizer(summarizer_id, summarizer, samples)

print('Done')