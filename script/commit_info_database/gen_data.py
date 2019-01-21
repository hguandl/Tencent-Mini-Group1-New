#/usr/bin/env python3

import os
from subprocess import run, PIPE

import pydbc
from parser import CtagsInfo, GitBlameInfo

REPO = '../../data/nginx'
CTAGS = '/usr/local/bin/ctags'

EXT = ['.c', '.cc', '.cpp']

def line_order(tag_info):
    return tag_info.get('line')

def find_func(info_list, line_num):
    if line_num < info_list[0].get('line'):
        return 'global'

    if info_list[-1].get('line') <= line_num:
        return info_list[-1].get('signature')

    l = 0
    r = len(info_list) - 1
    while l <= r:
        mid = (l + r) // 2
        if info_list[mid].get('line') == line_num:
            return info_list[mid].get('signature')

        if info_list[mid].get('line') < line_num and info_list[mid + 1].get('line') > line_num:
            return info_list[mid].get('signature')

        if info_list[mid].get('line') > line_num:
            r = mid

        if info_list[mid].get('line') < line_num:
            l = mid

    return 'global'


"""
def find_func(line_num):
    if (info_list[0].get('line')) > line_num:
        return 'global'

    if info_list[-1].get('line') <= line_num:
        return info_list[-1].get('signature')

    for i in range(len(info_list)):
        if info_list[i].get('line') <= line_num and info_list[i + 1].get('line') >= line_num:
            return info_list[i].get('signature')

    return 'global'
"""

obj = []

def main():
    explore(REPO)
    for i in range(len(obj)):
        print(f'[{i + 1}/{len(obj)}]\t{obj[i]}')
        process(obj[i])

def explore(path):
    global obj
    for entry in os.listdir(path):
        real_path = f'{path}/{entry}'
        if os.path.isfile(real_path):
            if os.path.splitext(entry)[1] in EXT:
                obj.append(real_path.replace(REPO + '/', ''))
        else:
            explore(real_path)

def process(file):
    # print(f'-------- {file} --------')

    info_list = []
    r = run([CTAGS, '-x', '--c-kinds=f', file], cwd=REPO, stdout=PIPE, stderr=PIPE)
    ctags_list = r.stdout.decode('UTF-8').split('\n')
    for line in ctags_list:
        if line == '':
            continue
        info_list.append(CtagsInfo(line))
    info_list.sort(key=line_order)


    blame_list = []
    r = run(['git', 'blame', '-c', '-l', file], cwd=REPO, stdout=PIPE, stderr=PIPE)
    git_list = r.stdout.decode('UTF-8').split('\n')
    for line in git_list:
        if line == '':
            continue
        blame_list.append(GitBlameInfo(line))

    # for i in range(len(blame_list)):
    #     print(f'line {i} is in function {find_func(i)}')

    function_set = { }
    for i in info_list:
        function_set[i.get('signature')] = []
    for i in blame_list:
        func = find_func(info_list, i.get('line'))
        if func == 'global':
            continue
        if i not in function_set[func]:
            function_set[func].append(i)

    for i in function_set:
        for j in function_set[i]:
            pydbc.add_record(j.get('hash'), j.get('author'), i, j.get('time'), file)


if __name__ == '__main__':
    pydbc.start()
    main()
    pydbc.close()