# 语法分析与栈展开

## 介绍

基于 Rust 编写，输入为 Clang 生成的 callgraph.dot 文件，输出是，该 callgraph 中所有存在的函数对 (A->B) 与 callgraph 中的对指定函数的栈展开算法，输出可能需要自己魔改下。

## 命令介绍

程序接受两个命令行参数，第一个是dot文件的路径，第二个是正则匹配文件的路径，正则匹配文件有3行，分别对应，整体图的名字(没啥用)，节点(函数)，节点间关系(函数call)。使用 cargo 运行即可。

​`cargo run dotfile.dot regexfile`

## 程序内部函数介绍

1. read_regex:  接受一个文件名为参数，返回一个含有该文件中的正则表达式的编译后版本的Vec。
2. analyse:  接受一个 dot 文件的内容（字符串格式），与使用的正则表达式 `Vec`，返回 `AnalysisRes` 结构体，其中包含有 `callpairs(HashMap<String, HashSet\<String\>>)` 和节点与函数名对应关系（`HashMap<String, String>`）
3. stack_expansion:  接受一个 `stack_trace(HashSet\<String\>)`，与之前的结构体(not implenmented)以及展开深度(u32)，返回栈展开路径上所有的函数(`HashSet\<String\>`)

