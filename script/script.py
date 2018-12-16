import requests
import json
from urllib import parse
from bs4 import BeautifulSoup
import math


def crash_report(product="Firefox", version="64.0rc1", nums_buck=1):
    # 初始化
    f = open('test.json', 'w', encoding='utf-8')
    bodies = {}
    functions = []

    crashes = []

    url = "https://crash-stats.mozilla.com/"
    url_1 = url + "topcrashers/"
    parameters_1 = {'product': product, 'version': version}
    get_1 = requests.get(url_1, params=parameters_1)  # 得到bucket名字
    get_1.encoding = 'utf-8'
    soup1 = BeautifulSoup(get_1.text, "html5lib")
    # buckets = soup1.find_all('a',attrs = {'class':'signature'})[(nums_buck-1):]
    # print(buckets[0].get_text())
    # 注意最大值(隐匿bug)
    for i in range(nums_buck):
        bucket = soup1.find_all('a', attrs={'class': 'signature'})[i]
        # print(bucket)
        url_2_bucket = bucket['title']
        url_2_bucket = parse.quote(url_2_bucket)
        url_2 = url + "/signature/reports/?product=Firefox&version=64.0rc1&signature=" + url_2_bucket + "&_columns=date&_columns=product&_columns=version&_columns=build_id&_columns=platform&_columns=reason&_columns=address&_columns=install_time&_sort=-date&page="
        get_2 = requests.get(url_2 + "1")  # 得到总页数
        get_2.encoding = 'utf-8'
        soup2 = BeautifulSoup(get_2.text, "html5lib")
        total_item = int(soup2.find_all('span', attrs={'class': 'totalItems'})[0].get_text().replace(',', ''))
        # print(total_item)
        pages = math.ceil(total_item / 50)  # 默认每页50个
        for j in range(pages):
            get_2 = requests.get(url_2 + str(j + 1))  # 得到crashing id
            get_2.encoding = 'utf-8'
            soup2 = BeautifulSoup(get_2.text, "html5lib")
            problems = soup2.find_all('a', attrs={'class': 'external-link crash-id'})[0:]
            for k in range(len(problems)):
                url_3 = url + problems[k]['href']
                get_3 = requests.get(url_3)  # 得到具体线程的crash stack
                get_3.encoding = 'utf-8'
                soup3 = BeautifulSoup(get_3.text, "html5lib")
                info = soup3.find_all('div', attrs={'id': 'details'})
                soup3 = BeautifulSoup(str(info), "html5lib")
                info = soup3.find_all(lambda tag: tag.name == 'table' and tag.get('class') == ['data-table'])
                if len(info) > 0:
                    # print(info)
                    crash = BeautifulSoup(str(info), "html5lib")
                    function = crash.find_all('td', title=True)[0:]
                    for i in range(len(function)):
                        functions.append(str(function[i]['title']))
                    function = crash.find_all('tr', attrs={'class': 'missingsymbols'})[0:]
                    crash = BeautifulSoup(str(function), "html5lib")
                    function = crash.find_all('td', title=True)[0:]
                    for i in range(len(function)):
                        crashes.append(str(function[i]['title']))
                    bodies['bucket'] = str(parse.unquote(url_2_bucket))
                    bodies['crash_id'] = str(problems[k])
                    bodies['crash_srack'] = functions
                    bodies['result'] = crashes
                    json.dump(bodies, f)
                    json.dump("\n", f)
                    functions = []
                    crashes = []
    f.close()


if __name__ == "__main__":
    crash_report()