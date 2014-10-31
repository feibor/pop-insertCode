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
	
	│        My work dirs and files..
	
	└── logs
	
		├── detail-2014-10-31.log
	
		├── duplicate-2014-10-31.log
	
		├── duplicate-more-2014-10-31.log
	
		├── error-2014-10-31.log
	
		├── ignore-2014-10-31.log
	
		├── info-2014-10-31.log
	
		├── nochange-2014-10-31.log
	
		└── warn-2014-10-31.log

2.可以设定需要执行的文件的扩展名，过滤规则扩展名以外的文件将不会被检索和执行

3.将会输出各种类型的日志，用以脚本执行完后的正确性参考，总共包含7中日志类型，详细如下：

		   1).detail 日志：

			detail是对执行过修改的所有文件列出详细情况，包括原有代码和修改后的代码（仅显示修改的那部分）

		   2).duplicate 日志：
			
			如果某个文件已经存在需要添加的代码（重复判定规则见headDuplicaetRule变量的值），则不对其进行修改，同时记录日志

		   3).duplicate-more 日志：
			   
			如果某个文件存在多个需要添加的代码（2个或两个以上，有可能是人工添加时，添加了重复的脚本），此时将会记录日志，用以提出警示，用户可通过日志来选择是否删除多余的代码

		   4).error 日志：
			    
			执行过程中，出现错误的文件将会被记录，同时记录错误异常信息

		   5).ignore 日志：
			
			过滤规则以外的文件将会忽略并记录日志。

		   6).no-change 日志：

			属于过滤规则以内的文件，但不存在head标签和body标签的文件将被记录日志，不修改其代码


		   7).warn 日志：
			
			某个文件存在多个head标签和body标签时，依然修改文件（所有的head标签 和body标签都会被加上想要插入的代码），但会记录警告日志，可由用户自行考虑是否修改。



Getting started:
  
  ```sh 
  python pop-insertcode.py /Users/ashihiroshi/Downloads/views/
  ```
  
  第一个参数是python的启用脚本语句，第二个参数是执行该脚本，第三个参数是需要插入代码的目录的路径。程序将会对 ```sh/Users/ashihiroshi/Downloads/views/ ```
  即，将对views目录进行遍历，在此之前会在脚本当前所在页生成 views_generator_时间戳
  为名称的文件夹，同时对views的目录进行备份并放在backup文件夹中，所有的生成的文件包括日志和备份都会放在该文件夹内。

  打开pop-insertcode.py脚本，可以根据个性化需要修改的相应参数详述如下：
  	
  filterRule常量：即过滤规则，filterRule是一个数组，表示脚本仅执行filterRule数组中所罗列的文件的扩展名（此处只针对扩展名，不针对具体文件），如果filterRule中没有数据，则将会对所有文件执行遍历
  	
 afterHead:即在head标签下将要添加的代码，如果不希望添加如下链接地址的js脚本代码，可以修改下面的值。
  	
 beforeBody：即在```</body>```标签之前添加相应代码
  	
 headDuplicaetRule:执行判重规则，即如果所述页面存在该值所对应的代码，则不会再进行相应添加，同时会记录相应日志，防止重复添加同样的代码。
  	
 bodyDuplicateRule:作用如headDuplicaetRule
  	
  	```python
  	version="v0.4Beta"

	argv = sys.argv;
	
	#扩展名过滤规则，即，只对.html扩展名的文件进行操作
	#File filter,you can add file type which you need,such as ".vm","jsp" etc...
	filterRule=['.html','.jsp'];
	
	#The code whitch I'll replace in all files;
	afterHead = '<script src="http://style.org.hc360.com/js/build/source/core/hc.common.js"></script>'
	
	beforeBody = '<script src="http://style.org.hc360.com/js/build/source/core/hc.control.js"></script>'
	
	#If some files had been insert the same code,these will not be changed again...
	headDuplicateRule='hc.common.js'
	bodyDuplicateRule='hc.control.js'
	
  	```
  
  
