# 代码数据库

记录某一函数都在哪些 commit 被修改过

## 原理

- 利用 [ctags](http://ctags.sourceforge.net) 获取代码的函数定义及位置

- 通过 `git blame` 信息获取某次函数的修改对应的具体作者和时间

- 结合以上信息生成关系型数据库

## 数据库驱动

```sh
$ pip3 install psycopg2-binary
```
