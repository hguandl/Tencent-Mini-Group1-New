import re
import os


def efficient_search(s, needNode=True):
    isNode = True if s.find('label=') != -1 else False
    if needNode != isNode:
        return None
    isRelation = True if s.find('->') != -1 else False
    if (not isRelation) and (not isNode):
        return None
    if isNode:
        node_s = s.find('Node')
        node_e = s.find(' [')
        label_s = s.find(r'"')
        label_e = s.find(r'",')
        return s[node_s:node_e], s[label_s:label_e]
    else:
        node1_s = s.find('Node')
        node1_e = s.find(' ->')
        node2_s = s.rfind('Node')
        node2_e = s.find(' [')
        return s[node1_s:node1_e], s[node2_s:node2_e]


def scan_path(path="/home/john/Downloads/test"):
    node_fn = {}
    node = []
    relation = {}
    files = os.listdir(path)
    for file in files:
        if not os.path.isdir(file):
            f = open(path+"/"+file)
            iter_f = iter(f)
            for line in iter_f:
                node_res = efficient_search(line)
                if node_res is not None:
                    node_name, label_name = node_res
                    label_name = label_name.replace(r'\l', '')
                    node.append(label_name)
                    node_fn[node_name] = label_name
                    relation[label_name] = relation.setdefault(label_name, set())
            f.seek(0)
            iter_f = iter(f)
            for line in iter_f:
                relation_res = efficient_search(line, False)
                if relation_res is not None:
                    s_node, e_node = relation_res
                    relation[node_fn[s_node]].add(node_fn[e_node])
    return node, relation


def stack_expansion(function_set, depth, relation):
    set_list = [set() for _ in range(depth)]
    set_list[0] = function_set
    for k in range(depth - 1):
        for function in set_list[k]:
            set_list[k+1] = set_list[k+1].union(relation[function])
    res = set()
    for s in set_list:
        res = res.union(s)
    return res


n, r = scan_path()
