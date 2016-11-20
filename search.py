import requests
import re


# import argparse

# parser = argparse.ArgumentParser(description='Get Google Count.')
# # parser.add_argument('word', help='word to count')
# args = parser.parse_args()


def google_search(word):
    r = requests.get('https://www.google.com.hk/search?q=\"'+word+'\"'
                     # params={'q':'"'+word+'"',
                     #         "tbs": "li:1"}
                    )

    if r.status_code == 200:
        data = r.text
        s = data.find("\"resultStats\"")
        ss = data[s:s + 100].find("</div>")
    else:
        print('Google gg, go bing')
        r = requests.get('https://www.bing.com/search?q=\"' + word + '\"')
        data = r.text
        s = data.find("\"sb_count\">")
        ss = data[s:s + 40].find("</span>")
        if r.status_code != 200:
            print ('Bing gg, go die')


    # soup = BeautifulSoup(r.text, "html.parser")
    # s = soup.find('div', {'id': 'resultStats'}).text

    ans = re.findall(r'\d+', data[s: s+ss])
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

