#/usr/bin/env python3

import os
from subprocess import run, PIPE

from parser import CtagsInfo, GitBlameInfo

SRC = '../../data/nginx/src/core'
CTAGS = '/usr/local/bin/ctags'

EXT = ['.c', '.cc', '.cpp']

info_list = []
blame_list = []

for file in os.listdir(SRC):
    if os.path.splitext(file)[1] not in EXT:
        continue
    r = run([CTAGS, '-x', '--c-kinds=f', file], cwd=SRC, stdout=PIPE, stderr=PIPE)
    ctags_list = r.stdout.decode('UTF-8').split('\n')
    for line in ctags_list:
        if line == '':
            continue
        info_list.append(CtagsInfo(line))
        print(info_list[-1].info)

    r = run(['git', 'blame', '-c', '-l', file], cwd=SRC, stdout=PIPE, stderr=PIPE)
    git_list = r.stdout.decode('UTF-8').split('\n')
    for line in git_list:
        if line == '':
            continue
        blame_list.append(GitBlameInfo(line))
        print(blame_list[-1].info)

