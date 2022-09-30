import base64
from urllib.parse import urlparse
import logging
import requests
import os


def fetch_file_from_git(git_url, path):
    # get the basics
    res = urlparse(git_url)
    try:
        _, user_name, repo = res.path.split('/')
    except ValueError:
        logging.error("couldn't split repo from %s" % git_url)
        return 0
    repo = repo.replace('.git', '')

    # authenticate for rate limiting
    auth_string = os.environ['GH_USERNAME'] + ':' + os.environ['GH_TOKEN']
    encoded = base64.b64encode(auth_string.encode('ascii'))
    headers = {
        "authorization" : 'Basic ' + encoded.decode('ascii'),
        "Accept"        : "application/vnd.github+json",
        }
    encoded = base64.b64encode(auth_string.encode('ascii'))

    api_url = 'https://api.github.com/repos/%s/%s/contents/%s' % (user_name, repo, path)

    logging.debug(api_url)
    r = requests.get(api_url, headers=headers)
    requests_remaining = int(r.headers['X-RateLimit-Remaining'])
    if requests_remaining == 0:
        logging.error("no API requests remaining")
        exit(1)

    logging.debug("API requests remaining %d" % requests_remaining)

    data = r.json()
    if 'content' not in data:
        return None

    file_content = data['content']

    file_content_encoding = data.get('encoding')
    if file_content_encoding == 'base64':
        file_content = base64.b64decode(file_content).decode()

    return file_content
