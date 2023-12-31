from jira import JIRA
from jira2markdown import convert
from markdown import markdown
from dotenv import load_dotenv
from os import environ
import pandas as pd

load_dotenv()

jira_base = environ.get('JIRA_BASE_URL')
jira_user = environ.get('JIRA_USER')
jira_api_token = environ.get('JIRA_API_TOKEN')

def get_all_issues_of_project(project: str) -> iter:
    jira_client = JIRA(jira_base, basic_auth=(jira_user, jira_api_token))
    chunk_size = 100
    start_at = 0

    while True:
        results = jira_client.search_issues(f'project = {project}', startAt=start_at, maxResults=chunk_size)

        if len(results.iterable) < 1:
            break

        yield from results.iterable

        start_at += chunk_size

    jira_client.close()


def get_all_assignees_of_project(project: str) -> iter:
    jira_client = JIRA(jira_base, basic_auth=(jira_user, jira_api_token))
    chunk_size = 100
    start_at = 0

    while True:
        results = jira_client.search_assignable_users_for_projects(username='', projectKeys=project, startAt=start_at, maxResults=chunk_size)

        if len(results.iterable) < 1:
            break

        yield from results.iterable

        start_at += chunk_size

    jira_client.close()

def convert_issue(issue):
    return {
        'id': issue.raw['id'],
        'self': issue.raw['self'],
        'key': issue.raw['key'],
        'description': markdown(convert(issue.raw['fields']['description'])) if issue.raw['fields']['description'] else '',
        'assignee': issue.raw['fields']['assignee'],
        'status': issue.raw['fields']['status'],
        'reporter': issue.raw['fields']['reporter']
    }

def convert_assignee(assignee):
    return assignee.raw

spam_issues = sorted(
    get_all_issues_of_project('DEBUG'),
    key=lambda issue: int(issue.raw['key'].split('-')[-1])
)
spam_issues = [convert_issue(issue) for issue in spam_issues]
pd.DataFrame(spam_issues).to_json('spam.json')
pd.DataFrame(spam_issues).to_csv('spam.csv')

support_issues = sorted(
    get_all_issues_of_project('SUPIT'),
    key=lambda issue: int(issue.raw['key'].split('-')[-1])
)
support_issues = [convert_issue(issue) for issue in support_issues]
pd.DataFrame(support_issues).to_json('issues.json')
pd.DataFrame(support_issues).to_json('issues.csv')

assignees = [convert_assignee(assignee) for assignee in get_all_assignees_of_project('SUPIT')]
pd.DataFrame(assignees).to_json('assignees.json')
pd.DataFrame(assignees).to_csv('assignees.csv')
