#/usr/bin/env python3

import os
import shutil


class CtagsInfo(object):
    def __init__(self, raw_str):
        self.pt = 0
        self.raw_str = raw_str
        self.info = { }
        self._find(None)
        self._find(None)
        self._find('line')
        self._find('filename')
        self._find('signature')

    def __seek(self) -> int:
        pt = self.pt
        while self.raw_str[pt:pt + 1] == ' ':
            pt += 1
        return pt
        
    def __next(self, name) -> int:
        if name == 'signature':
            return None
        pt = self.pt
        while self.raw_str[pt:pt + 1] != ' ':
            pt += 1
        return pt

    def _find(self, name) -> str:
        self.pt = self.__seek()
        end = self.__next(name)
        self.pt = end
        self.info[name] = self.raw_str[self.pt:end]

    def get(self, key):
        return self.info.get(key)


class GitBlameInfo(object):
    __tab_map = {
        'hash': 0,
        'author': 1,
        'time': 2,
        'line': 3
    }

    def __trim(s, name):
        if name == 'author':
            return s[1:]
        if name == 'line':
            return s[:s.find(')')]
        return s

    def __init__(self, raw_str):
        raw_info = raw_str.split('\t')
        self.info = { }
        self.__process_info(raw_info)

    def __process_info(self, raw_info):
        for k in GitBlameInfo.__tab_map:
            self.info[k] = GitBlameInfo.__trim(raw_info[GitBlameInfo.__tab_map[k]], k)

    def get(self, key):
        return self.info.get(key)

