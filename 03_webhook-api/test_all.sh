#!/bin/sh

python3 test_summarization.py distilbart ./samples_for_summarization_testing_cleaned.json
python3 test_summarization.py flan_t5 ./samples_for_summarization_testing_cleaned.json
python3 test_summarization.py bart_facebook ./samples_for_summarization_testing_cleaned.json
python3 test_summarization.py bart_custom ./samples_for_summarization_testing_cleaned.json
python3 test_summarization.py pegasus_xsum ./samples_for_summarization_testing_cleaned.json
python3 test_summarization.py pegasus_samsum ./samples_for_summarization_testing_cleaned.json

echo 'DONE'