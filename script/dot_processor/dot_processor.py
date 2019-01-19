import csv
import os
import re
import sys
csv.field_size_limit(sys.maxsize)


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
        return s[node_s:node_e], s[label_s + 1:label_e]
    else:
        node1_s = s.find('Node')
        node1_e = s.find(' ->')
        node2_s = s.rfind('Node')
        node2_e = s.find(' [')
        return s[node1_s:node1_e], s[node2_s:node2_e]


def scan_path(path):
    node_fn = {}
    node = []
    relation = {}
    files = os.listdir(path)
    for file in files:
        if not os.path.isdir(file):
            f = open(path + "/" + file)
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


def write2dot(pypath, dotpath, node_list, relation_dict):
    node_index = {}
    count = 0
    with open(dotpath, 'w') as file:
        file.write('digraph "Firefox"\n')
        file.write('\n{')
        for node in node_list:
            file.write('node{}[label="{}"]'.format(count, node))
            node_index[node] = count
            count += 1
        for node in node_list:
            for e_node in relation_dict[node]:
                file.write('node{}->node{}\n'.format(node_index[node], node_index[e_node]))
        file.write('}')
        file.close()
    with open(pypath, 'w') as file:
        file.write('node_index={}\n'.format(str(node_index)))
        file.write('node_list={}\n'.format(str(node_list)))
        file.write('relation_dict={}\n'.format(str(relation_dict)))
        file.close()
    print('Total {} nodes, {} edges processed'.format(count, len(relation_dict)))


def stack_expansion(function_set, depth, relation):
    set_list = [set() for _ in range(depth)]
    depth_dict = {}
    set_list[0] = function_set
    for func in set_list[0]:
        depth_dict[func] = 0
    for k in range(depth - 1):
        for function in set_list[k]:
            set_list[k + 1] = set_list[k + 1].union(relation[function])
            for callee in relation[function]:
                depth_dict[callee] = k + 1
    res = set()
    for s in set_list:
        res = res.union(s)
    return res, depth_dict


def extract_func(s, func_idx):
    s_list = eval(s)
    res = []
    depth_dict = {}
    func_re = re.compile(r'.* (?P<function_name>[\w_:]+)\(.*\)')
    count = 1
    for s in s_list:
        temp = func_re.search(s)
        if (temp is not None) and (func_idx.get(temp.group('function_name')) is not None):
            res.append(temp.group('function_name'))
            depth_dict[temp.group('function_name')] = count
            count += 1
    return res, depth_dict


def stacktrace_process(n, r, stacktrace_path='test.csv'):
    with open(stacktrace_path, 'r') as file:
        traces = []
        dis_dict = {}
        st_reader = csv.DictReader(file, quoting=1,
                                   lineterminator='\n',
                                   delimiter='\t')
        for row in st_reader:
            (expanded_st, cg_depth) = extract_func(row['crash_stack'], n)
            (res, depth_dict) = stack_expansion(expanded_st, 5, r)
            traces.append(res)
            for key in depth_dict:
                dis_dict[key] = dis_dict.setdefault(key, 0) + depth_dict[key] + cg_depth.setdefault(key, 0)
        return traces, dis_dict


def statistic_process(dis_dict, traces):
    func_list = set()
    func_count = {}
    func_score = {}
    for trace in traces:
        func_list = func_list.union(trace)
    for trace in traces:
        for func in trace:
            func_count[func] = func_count.setdefault(func, 0) + 1
    for key in func_count.keys():
        func_score[key] = func_count[key] / len(func_list) * func_count[key] / (1 + dis_dict[key])
    return func_score


node_index = {}
relation_dict = {}
exec(open('data.py', 'rb').read())
(t, d) = stacktrace_process(node_index, relation_dict)
res = statistic_process(d, t)
print(res)
