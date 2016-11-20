import requests
from bs4 import BeautifulSoup
import re
import run_shell

# import argparse

# parser = argparse.ArgumentParser(description='Get Google Count.')
# # parser.add_argument('word', help='word to count')
# args = parser.parse_args()


def google_search(word):
    r = requests.get('http://www.google.com/search',
                     params={'q':'"'+word+'"',
                             "tbs": "li:1"}
                    )
    print r
    soup = BeautifulSoup(r.text, "html.parser")
    s = soup.find('div', {'id': 'resultStats'}).text
    ans = re.findall(r'\d+', s)
    num = 0
    for i in range(0, len(ans)):
        num = num * 1000 + int(ans[i])

    print word, num
    return num
#
# def Google_scraper_search(word):
#     run_shell.run_Google_Scraper_shell(word)
#     #
#     # return num

