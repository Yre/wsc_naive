import requests
from bs4 import BeautifulSoup
import re
import run_shell

# import argparse

# parser = argparse.ArgumentParser(description='Get Google Count.')
# # parser.add_argument('word', help='word to count')
# args = parser.parse_args()


def google_search(word):
    r = requests.get('https://www.google.com/search?q=\"'+word+'\"'
                     # params={'q':'"'+word+'"',
                     #         "tbs": "li:1"}
                    )
    print r

    if r.status_code != 200:
        print('Google gg')

    # soup = BeautifulSoup(r.text, "html.parser")
    # s = soup.find('div', {'id': 'resultStats'}).text
    data = r.text
    print data
    s = data.find("\"resultStats\"")
    print s
    ans = re.findall(r'\d+', data[s, s+100])
    print "ans=", ans
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

