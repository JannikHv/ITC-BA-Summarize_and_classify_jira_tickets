import os
import sys
import json
from src.helper import TextHelper

def print_help():
    print('Usage: python3 test_summaries.py <issues.json>')

issues_export_filepath = sys.argv[-1]

if not os.path.isfile(issues_export_filepath):
    print_help()
    quit(-1)


issues = json.load(open(issues_export_filepath, 'r'))
words = [
    TextHelper.count_words(TextHelper.clean_text(issue['description']))
    for issue in issues
    if issue['description']
]
characters = [
    len(TextHelper.clean_text(issue['description']))
    for issue in issues
    if issue['description']
]

print(f'Average issue words: {round(sum(words) / len(words))}')
print(f'Average issue length: {round(sum(characters) / len(characters))}')