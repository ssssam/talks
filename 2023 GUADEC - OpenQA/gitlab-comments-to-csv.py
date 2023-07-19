import csv
from datetime import datetime
import os
from gitlab import Gitlab

# Gitlab API endpoint and access token
GITLAB_URL = 'https://gitlab.gnome.org/'  # Replace with your Gitlab instance URL
PRIVATE_TOKEN = os.environ['GITLAB_PRIVATE_TOKEN']

# Project ID and issue IID
PROJECT_ID = 17928
ISSUE_IID = 9

def fetch_comments(api):
    prj = api.projects.get(PROJECT_ID)
    issue  = prj.issues.get(ISSUE_IID)
    comments = issue.notes.list(get_all=True)

    comment_data = []
    for comment in comments:
        comment_data.append({
            'created_at': datetime.fromisoformat(comment.created_at).strftime('%Y-%m-%d'),
            'body': comment.body,
        })

    return comment_data

def save_to_csv(comment_data):
    headers = ['created_at', 'body']

    with open('gitlab_issue_comments.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(comment_data)

if __name__ == '__main__':
    import logging, sys
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    gl = Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)

    try:
        comments_data = fetch_comments(gl)
        save_to_csv(comments_data)
        print('Comments fetched successfully and saved to gitlab_issue_comments.csv')
    except Exception as e:
        print(f'Error occurred: {e}')
