#/usr/bin/env python3

class CtagsInfo(object):
    __tab_list = [
        None,
        None,
        'line',
        'filename',
        'signature'
    ]

    def __init__(self, raw_str):
        self.pt = 0
        self.raw_str = raw_str
        self.info = { }
        for i in range(len(CtagsInfo.__tab_list)):
            self._find(i)

    def __seek(self) -> int:
        pt = self.pt
        while self.raw_str[pt:pt + 1] == ' ':
            pt += 1
        return pt
        
    def __next(self) -> int:
        pt = self.pt
        while self.raw_str[pt:pt + 1] != ' ':
            pt += 1
        return pt

    def _find(self, idx):
        self.pt = self.__seek()
        if idx == len(CtagsInfo.__tab_list) - 1:
            end = None
        else:
            end = self.__next()
        if CtagsInfo.__tab_list[idx] is not None:
            if CtagsInfo.__tab_list[idx] == 'line':
                self.info[CtagsInfo.__tab_list[idx]] = int(self.raw_str[self.pt:end])
            else:
                self.info[CtagsInfo.__tab_list[idx]] = self.raw_str[self.pt:end]
        self.pt = end

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
            return int(s[:s.find(')')])
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

    def __eq__(self, other):
        return self.get('hash') == other.get('hash')
