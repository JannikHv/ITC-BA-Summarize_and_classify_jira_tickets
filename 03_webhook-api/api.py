from flask import Flask, request, jsonify
from os import environ
from jira import JIRA
from dotenv import load_dotenv
from threading import Thread
from functools import wraps
from src.text_summarization import BartCustomSummarizer
from src.text_translation import DeToEnTranslator, EnToDeTranslator
from src.spam_classification import RobertaSpamClassifier

load_dotenv()

app = Flask(__name__)
debug = environ.get('DEBUG') == '1'
port = environ.get('PORT', '8080')
host = environ.get('HOST', '0.0.0.0')
api_key = environ.get('API_KEY', None)
jira_base_url = environ.get('JIRA_BASE_URL')
jira_user = environ.get('JIRA_USER')
jira_access_token = environ.get('JIRA_ACCESS_TOKEN')
jira = JIRA(
    server=jira_base_url,
    basic_auth=(jira_user, jira_access_token)
)
summarizer = BartCustomSummarizer(
    de_to_en_translator=DeToEnTranslator(),
    en_to_de_translator=EnToDeTranslator()
)
spam_classifier = RobertaSpamClassifier(
    de_to_en_translator=DeToEnTranslator()
)

def require_api_key(api_key: str):
    def decorator(func: callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = request.args.get('key')

            if not key or key != api_key:
                return jsonify({ }), 401

            return func(*args, **kwargs)

        return wrapper

    return decorator

def process_webhook_data(webhook_data: dict):
    data = webhook_data['issue']
    key = data['key']
    description = data['fields']['description']
    summary = summarizer.summarize(description)
    spam = spam_classifier.classify(description).spam
    comment = '\n'.join([
        f'Spam-Wahrscheinlichkeit: {round(spam, 2)} %\n'
        f'Zusammenfassung:\n{summary}'
    ])

    jira.add_comment(issue=key, body=comment)

@app.route('/', methods=['GET'])
def index():
    return jsonify({ 'message': 'API is running' }), 200

@app.route('/webhook/jira/issue/created', methods=['POST'])
@require_api_key(api_key=api_key)
def on_jira_issue_created():
    Thread(
        target=process_webhook_data,
        args=(request.get_json(),)
    ).start()

    return jsonify({ }), 200

if __name__ == '__main__':
    app.run(debug=debug, port=int(port), host=host)
