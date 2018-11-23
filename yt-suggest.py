import argparse

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

"""
Example tag of suggestion
<a class=" content-link spf-link yt-uix-sessionlink spf-link " data-sessionlink="itct=CC8QpDAYACITCP70zZDJ390CFYxcYAodzwIH2Cj4HTIHYXV0b25hdkiI95em1u2g_u0B" data-visibility-tracking="CC8QpDAYACITCP70zZDJ390CFYxcYAodzwIH2Cj4HUCF04PHrNqE-rsB" href="/watch?v=u_QS0sjg6YU" rel=" spf-prefetch nofollow" title="【OFFICIAL】 NicoNico Music Party 2015 VOCALOID Live">
"""

SUGG_CLASS = " content-link spf-link yt-uix-sessionlink spf-link "
YT_PREFIX = 'https://www.youtube.com'
CHAR_LIMIT = 100
LONG_BOI = '-'*CHAR_LIMIT

class Error(Exception):
    pass

class BadHTMLError(Error):
    """Exception raised for error in HTML received from URL

    Attributes:
        message -- explanation of error
    """

    def __init__(self, message):
        self.message = message

# Terminal colours
# https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
class bcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# STOLEN
# stolen from https://realpython.com/python-web-scraping-practical-introduction/

def get_url(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                raise BadHTMLError

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

#
# NELOTS

def main():
    # Parse args
    parser = argparse.ArgumentParser(
            description='Get the suggested videos from a youtube url')

    parser.add_argument('yt_url', metavar='yt_url', type=str, nargs='?', 
            default='https://www.youtube.com/watch?v=dQw4w9WgXcQ', 
            help='url of the youtube page to get')

    parser.add_argument('-v', '--verbose', action='store_true',
            help='Pretty Print the output with YouTube prefix and title')

    parser.add_argument('-p', '--prefix', action='store_true',
            help='Prefix the output with YouTube prefix')

    args = parser.parse_args()

    # Check url
    if args.yt_url.startswith(YT_PREFIX) == False:
        log_error('Please use a YouTube URL!')

    #print('Got youtube url: '+args.yt_url)

    # (try) Make soup
    try:
        html = BeautifulSoup(get_url(args.yt_url), 'html.parser')
    except BadHTMLError as e:
        log_error(e.message)

    # Find classes
    if args.verbose:
        for a in html.find_all('a', class_=SUGG_CLASS):
            link = YT_PREFIX+a['href']

            print(LONG_BOI)
            print(bcol.BOLD + bcol.HEADER 
                    + 'Title: ' + a['title'] 
                    + bcol.ENDC)
            print(bcol.UNDERLINE + bcol.OKBLUE 
                    + 'Link: ' + link 
                    + bcol.ENDC)
        print(LONG_BOI)

    else:
        for a in html.find_all('a', class_=SUGG_CLASS):
            if args.prefix:
                link = YT_PREFIX+a['href'] 
            else:
                link = a['href'].split('=')[1]

            print(link)

if __name__ == '__main__':
    main()

