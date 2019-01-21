# Commit 相关信息构成的数据库

关浩

- 表结构
	* 表之间的关系可参照 db_schema.jpg。
	* 本次采用的是 PostgreSQL 11 数据库，建表语句在 postgres_create.sql 内。

- 数据集  
	使用 Nginx 作为案例，纯 C 编写。

- 数据库内容  
	数据库相关配置在 database.cnf 中，由于只能在内网访问，因此导出了一份数据库内容存在 tencent.dump 中。

- 过程演示  
	由于视频较大，放到了 [Release](https://github.com/hguandl/Tencent-Mini-Group1-New/releases) 中，名为 db_create.mp4。
