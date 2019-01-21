# 代码数据库
记录某一函数都在哪些 commit 被修改过

关浩

## 原理

- 利用 [ctags](http://ctags.sourceforge.net) 获取代码的函数定义及位置

- 通过 `git blame` 信息获取某次函数的修改对应的具体作者和时间

- 结合以上信息生成关系型数据库

## 代码
- parser.py  
	格式化 ctags 输出和 git blame 输出
- gen_data.py  
	遍历 Git 仓库，对代码⽂文件分别调⽤用 ctags 和 git blame 进⾏行行处理理，⽣生成输出信息
- pydbc.py  
 	连接数据库，插⼊入新的信息条⽬。

## 数据库驱动

```sh
$ pip3 install psycopg2-binary
```

## 使用方法
1. 根据 `data/postgres_create.sql` 建立数据库
2. 在 `pydbc.py` 中设置好数据库连接信息
3. 在 `gen_data.py` 中设置要分析的仓库路径 `REPO`、Exuberant Ctags 路径 `CTAGS` 和要处理的文件拓展名 `EXT`
4. 运行 `gen_data.py`
