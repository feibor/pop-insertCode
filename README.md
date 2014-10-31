pop-insertCode
==============

This is a python script ,which can loop your workdirs ,and insert codes to some kind of files.Under works will describe in two kinds of languages

##Chinese:
 下面大概说一下一些核心的信息,这个脚本因为可以用来分析目录下的各种文件，所以打算等时间空闲了做成一些比较实用的小工具，预计0.5 Release版本将分离出一些功能。如可支持过滤特定文件名称或目录（目前仅支持对指定扩展名的文件进行遍历，不支持通配符）等。

建议：本脚本会自动备份将要执行的目录，放在backup文件夹中，自己测试没发现什么问题，不过仍然建议执行前先备份原有目录。
	
Do you know?
	
1.该脚本会对将要执行的文件夹进行自动备份，虽然本脚本将不会覆盖原有目录,而是在脚本所在目录重新生成一个目录，并将目标文件夹完全按照原有的目录结构复制出来。
	
 如下所示：其中我此次执行的目录是views目录，其中logs是存放日志，backup存放备份，
	├── backup
│   └── buyerInfoSearch_backup20141031163523.tar.gz
├── buyerInfoSearch
│   ├── areaIssueQuery.html
│   ├── assignSimpleList.html
│   ├── belongList.html
│   ├── infoExport.html
│   ├── test
│   │   ├── mySimpleList.html
│   │   ├── procureQuery.html
│   │   └── pubSimpleList.html
│   ├── test.html
│   ├── test2
│   │   └── ni1
│   ├── test3
│   │   └── ni344
│   └── test4
│       └── ni355
└── logs
    ├── detail-2014-10-31.log
    ├── duplicate-2014-10-31.log
    ├── duplicate-more-2014-10-31.log
    ├── error-2014-10-31.log
    ├── ignore-2014-10-31.log
    ├── info-2014-10-31.log
    ├── nochange-2014-10-31.log
    └── warn-2014-10-31.log
