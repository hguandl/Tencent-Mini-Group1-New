# dot 文件处理以及统计学计算部分文档

----

本文件统计学计算怀疑度实现参考 CrashLocator，dot 文件生成参考 doxygen 文档生成系统，本程序实现了对多个独立文件生成的 call graph 文件进行整合，生成整个程序的 call graph 文件的功能以及对整个程序的文件进行解析，根据堆栈得到怀疑度的功能。

## dot文件处理部分

---

1. `eficient_search` 函数  
   获取一个行中可能含有的信息，结果分为两种，当对应的行是 node 定义时，返回 node 的编号与标签，当对应的行是 node 间关系时，返回起始 node 与终止 node。

2. `scan_path` 函数  
   对一个路径下所有.dot文件进行遍历，并且调用`efficient_search`函数生成总体的call graph文件。返回全局的node定义以及node间关系。

3. `stack_expansion` 函数  
   对一个堆栈信息进行展开，生成所有可能的 fail trace，并且生成各个函数在对应的 fail trace 中的深度，用于后续统计学中的深度分析。

4. `stack_process` 函数  
   根据上面函数生成的信息进行整合，生成所有可能的 traces 以及对应的深度。

5. `statistic_process` 函数  
   对所有可能的 traces，按照 CrashLocator 的公式对每个函数计算怀疑度，返回一个函数对应怀疑度的字典。
  