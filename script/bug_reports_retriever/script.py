import requests
import csv
from urllib import parse
from bs4 import BeautifulSoup
import math


def crash_report(product="Firefox", version="64.0.2", nums_buck=1, url_2_bucket="bye"):
    # 初始化
    f = open('test.csv', 'w', encoding='utf-8', newline='')
    headers = ['bucket', 'crash_id', 'crash_stack', 'other_stack']

    f_csv = csv.DictWriter(f, headers, 
        quoting=1,
        lineterminator='\n',
        delimiter='\t'
        )
    f_csv.writeheader()
    bodies = dict()
    functions = []
    other_functions = []
    url="https://crash-stats.mozilla.com/"
    if url_2_bucket == "bye":
        url_1 = url+"topcrashers/?product="+product+"&version="+version
        get_1 = requests.get(url_1)  # 目的：得到bucket名字
        get_1.encoding = 'utf-8'
        soup1 = BeautifulSoup(get_1.text, "html5lib")
        # 注意最大值(隐匿bug)
        for i in range(0, nums_buck):
            bucket = soup1.find_all('a', attrs={'class': 'signature'})[i]
            # print(bucket)
            url_2_bucket = bucket['title']
            url_2_bucket = parse.quote(url_2_bucket)
            url_2 = url+"/signature/reports/?product="+product+"&version="+version+"&signature="+url_2_bucket + \
                    "&_columns=date&_columns=product&_columns=version&_columns=build_id&_columns=platform&_columns=reason&_columns=address&_columns=install_time&_sort=-date&page="
            get_2 = requests.get(url_2+"1")  # 得到总页数
            get_2.encoding = 'utf-8'
            soup2 = BeautifulSoup(get_2.text, "html5lib")
            total_item = int(soup2.find_all('span', attrs={'class': 'totalItems'})[0].get_text().replace(',', ''))
            # print(total_item)
            pages = math.ceil(total_item/50)  # 默认每页50个
        for j in range(1, pages):
            get_2 = requests.get(url_2+str(j+1))  # 得到crashing id
            get_2.encoding = 'utf-8'
            soup2 = BeautifulSoup(get_2.text,"html5lib")
            problems = soup2.find_all('a', attrs={'class':'external-link crash-id'})[0:]
            for k in range(len(problems)):
                url_3 = url+problems[k]['href']
                get_3 = requests.get(url_3)  # 得到具体线程的crash stack
                get_3.encoding = 'utf-8'
                soup3 = BeautifulSoup(get_3.text, "html5lib")
                info = soup3.find_all('div', attrs={'id': 'frames'})
                soup3 = BeautifulSoup(str(info), "html5lib")
                info = soup3.find_all(lambda tag: tag.name == 'table' and tag.get('class') == ['data-table'])
                if len(info) > 0:
                    crash_info = info[0]
                    crash = BeautifulSoup(str(crash_info), "html5lib")
                    function = crash.find_all('tr')[0:]
                    for g in range(len(function)):
                        crash = BeautifulSoup(str(function[g]), "html5lib")
                        a_num = crash.find_all('a')
                        if len(a_num) > 0:
                            function_1 = function[g].find_all('td', title=True)
                            functions.append(str(function_1[0]['title']))
                    if len(info) > 1:
                        other_info = info[1:]
                        other_crash = BeautifulSoup(str(other_info), "html5lib")
                        other_function = other_crash.find_all('tr')[0:]
                        for g in range(len(other_function)):
                            other_crash = BeautifulSoup(str(other_function[g]), "html5lib")
                            other_a_num = other_crash.find_all('a')
                            if len(other_a_num) > 0:
                                other_function_1 = other_function[g].find_all('td', title=True)
                                other_functions.append(str(other_function_1[0]['title']))
                    if len(functions) > 0:
                        bodies['bucket'] = str(parse.unquote(url_2_bucket))
                        bodies['crash_id'] = str(problems[k]['href'])
                        bodies['crash_stack'] = functions
                        bodies['other_stack'] = other_functions
                        f_csv.writerow(bodies)
                print(url_3)
                functions = []
    else:
        url_2_bucket = parse.quote(url_2_bucket)
        url_2 = url+"/signature/reports/?product="+product+"&version="+version+"&signature="+url_2_bucket + \
                "&_columns=date&_columns=product&_columns=version&_columns=build_id&_columns=platform&_columns=reason&_columns=address&_columns=install_time&_sort=-date&page="
        get_2 = requests.get(url_2+"1")  # 得到总页数
        get_2.encoding = 'utf-8'
        soup2 = BeautifulSoup(get_2.text, "html5lib")
        total_item = int(soup2.find_all('span', attrs={'class': 'totalItems'})[0].get_text().replace(',', ''))
        # print(total_item)
        pages = math.ceil(total_item/50)  # 默认每页50个
        for j in range(pages):
            get_2 = requests.get(url_2+str(j+1))  # 得到crashing id
            get_2.encoding = 'utf-8'
            soup2 = BeautifulSoup(get_2.text, "html5lib")
            problems = soup2.find_all('a', attrs={'class': 'external-link crash-id'})[0:]
            for k in range(len(problems)):
                url_3 = url+problems[k]['href']
                get_3 = requests.get(url_3)  # 得到具体线程的crash stack
                get_3.encoding = 'utf-8'
                soup3 = BeautifulSoup(get_3.text,"html5lib")
                info = soup3.find_all('div',attrs={'id':'frames'})
                soup3 = BeautifulSoup(str(info),"html5lib")
                info = soup3.find_all(lambda tag: tag.name == 'table' and tag.get('class') == ['data-table'])
                if len(info) > 0:
                    crash_info = info[0]
                    crash = BeautifulSoup(str(crash_info), "html5lib")
                    function = crash.find_all('tr')[0:]
                    for g in range(len(function)):
                        crash = BeautifulSoup(str(function[g]), "html5lib")
                        a_num = crash.find_all('a')
                        if len(a_num) > 0:
                            function_1 = function[g].find_all('td' , title=True)
                            functions.append(str(function_1[0]['title']))
                    if len(info) > 1:
                        other_info = info[1:]
                        other_crash = BeautifulSoup(str(other_info), "html5lib")
                        other_function = other_crash.find_all('tr')[0:]
                        for g in range(len(other_function)):
                            other_crash = BeautifulSoup(str(other_function[g]), "html5lib")
                            other_a_num = other_crash.find_all('a')
                            if len(other_a_num) > 0:
                                other_function_1 = other_function[g].find_all('td', title=True)
                                other_functions.append(str(other_function_1[0]['title']))
                    if len(functions) >0:
                        for i in range(0, len(function)):
                            bodies['bucket'] = str(parse.unquote(url_2_bucket))
                            bodies['crash_id'] = str(problems[k]['href'])
                            bodies['crash_stack'] = functions.pop()
                            bodies['other_stack'] = other_functions.pop()
                            f_csv.writerow(bodies)
                print(url_3)
                functions = []
                other_functions = []
    f.close()


if __name__ == "__main__":
    crash_report()
