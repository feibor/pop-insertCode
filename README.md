pop-insertCode
==============

This is a python script ,which can loop your workdirs ,and insert codes to some kind of files(I think it also can be used to search some words in a mass of files quickly ).

##For example:

  My company get an user behavior analysis javascript one day ago .But our old web project haven't this javascript code.
  
  Then,my boss mails me and say:
 ``` 
  Hi Lee,
       Today we get an user behavior anaysis javascript ,so you shoud add this javascript reference to 
     all old projects before 20xx-xx-xx(I only have 20 days to do this work!),and of courese it is an 
     milestone for us,so please do your best 
     to resolve this problem.
     
     Thanks
  ```   
  Oh.. My God!We have 20 projects more,and each project maybe have more about 20000 files !It means that ,I must take a very 
very long,boring,irritability time to insert the javascript reference!

  But,fortunately,I write a python script to do all of these works,no error,no boring,quickly,effectively.So , I share my script to solve others trouble...

Below words will describe in two kinds of languages,just follow your favour.

##Chinese:
 下面大概说一下一些核心的信息,这个脚本因为可以用来分析目录下的各种文件，所以打算等时间空闲了做成一些比较实用的小工具，预计0.5 Release版本将分离出一些功能。如可支持过滤特定文件名称或目录（目前仅支持对指定扩展名的文件进行遍历，不支持通配符）等。

建议：本脚本会自动备份将要执行的目录，放在backup文件夹中，自己测试没发现什么问题，不过仍然建议执行前先备份原有目录。
	
Do you know?
	
1.该脚本会对将要执行的文件夹进行自动备份，虽然本脚本将不会覆盖原有目录,而是在脚本所在目录重新生成一个目录，并将目标文件夹完全按照原有的目录结构复制出来。
	
 如下所示：其中我此次执行的目录是buyerInfoSearch目录，其中logs是存放日志，backup存放备份，
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
  python pop-insertcode.py /Users/ashihiroshi/Downloads/buyerInfoSearch/
  ```
  
  第一个参数是python的启用脚本语句，第二个参数是执行该脚本，第三个参数是需要插入代码的目录的路径。程序将会对 ```sh/Users/ashihiroshi/Downloads/buyerInfoSearch/ ```
  即，将对buyerInfoSearch目录进行遍历，在此之前会在脚本当前所在页生成 buyerInfoSearch_generator_时间戳
  为名称的文件夹，同时对buyerInfoSearch的目录进行备份并放在backup文件夹中，所有的生成的文件包括日志和备份都会放在该文件夹内。

  打开pop-insertcode.py脚本，可以根据个性化需要修改的相应参数详述如下：
  	
  filterRule常量：即过滤规则，filterRule是一个数组，表示脚本仅执行filterRule数组中所罗列的文件的扩展名（此处只针对扩展名，不针对具体文件），如果filterRule中没有数据，则将会对所有文件执行遍历
  	
 afterHead:即在head标签下将要添加的代码，如果不希望添加如下链接地址的js脚本代码，可以修改下面的值。
  	
 beforeBody：即在```</body>```标签之前添加相应代码
  	
 headDuplicaetRule:执行判重规则，即如果所述页面存在该值所对应的代码，则不会再进行相应添加，同时会记录相应日志，防止重复添加同样的代码。
  	
 bodyDuplicateRule:作用如headDuplicaetRule
  	

  	#!/usr/bin/env python
  	version="v0.4Beta"

	argv = sys.argv;
	
	#扩展名过滤规则，即，只对.html扩展名的文件进行操作
	#File filter,you can add file type which you need,such as ".vm","jsp" etc...
	filterRule=['.html','.jsp'];
	
	#The code whitch I'll replace in all files;
	afterHead = '<script src="hc.common.js"></script>'
	
	beforeBody = '<script src="hc.control.js"></script>'
	
	#If some files had been insert the same code,these will not be changed again...
	headDuplicateRule='hc.common.js'
	bodyDuplicateRule='hc.control.js'
	

  执行效果如下：
  ```
|-----------------------------------------------------------------------|
|                PopInsertCode Version: v0.4Beta                        |
|                @Author:Andrew Lee                                     |
|                @Email:lipengfei217@163.com                            |
|                @GitHub:https://github.com/lipengfei217                |
|-----------------------------------------------------------------------|

Caculating quantity of all files,please wait....
-----------------------------------------------------------------------
                 TotalFiles： 12
-----------------------------------------------------------------------
 Now is creating a bakup，please wait for minutes......
tar -czvf buyerInfoSearch_generator20141031163523/backup/buyerInfoSearch_backup20141031163523.tar.gz buyerInfoSearch/


-------------Backup accomplish ,path is /Users/ashihiroshi/Workspaces/pythonSpace/work/userActiveCode/src/buyerInfoSearch_generator20141031163523/backup/buyerInfoSearch_backup20141031163523.tar.gz

Create folder :buyerInfoSearch_generator20141031163523/logs
Create folder :buyerInfoSearch_generator20141031163523/code

Executed Files：12 | Changed Files：8 | Remaining Files：0 | Faild Files：0 | 100%  ||====================================================================================================->

Program Over

  Program Over

```

图中会实时显示执行的进度，具体含义如下所述：
	
  a. Executed Files:当前已经执行过的文件数

  b. Changed Files:当前已经执行过的且符合filterRule过滤规则的文件数，即 Changed Files = 文件总数-到当前为止不符合过滤规则的文件数

  c.Remaining Files:当前剩余的还需要执行的文件

  d.Faild Files:报错的文件数，通常如果执行某个文件时出现脚本错误等，次数将会+1并记录日志。


##English:

 Below will describe some core infomation about this python script.I think this script can be used to analysis some files which under a work folder.So if idle ,on the basis of this script, I'll do some futhur work to get some convenience utils.
 
 warning:This script will auto bakup your work dirs,and put it into a folder which named backup,but because of no enough test,I suggest that you should backup your work dirs first,although I don't think it is necessary.
 
 __Documentation__
 
 Do you know?
 
 1.Program will auto backup your work dir first，and will not revert your work dir.It will create an copy of your files and
 dirs under your work dir,of course ,folders' levels will as the same as your work dir.
 
 As the codes show below：buyerInfoSearch is my work dir,work dir path is ```/Users/ashihiroshi/Downloads/buyerInfoSearch/```
 
 the buyerInfoSearch_generator20141031163523 folder will be created under your current shell path.
 
    ├── buyerInfoSearch_generator20141031163523
    
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

2.You can indicate file's extensions,Out of filter rule of file's extensions will not be done.

3.Program will output a lot kinds of logs for you to check some mistaks of new files. 7 kinds of logs will be gived under ```logs``` directory.Detail information will be gived bellow:

  1).```detail``` log ： 
  
    Detail log will list all of files which have been changed ,further more, will code has been changed and changed to what will also been given in this log.
    
  2).```duplicate``` log:
  
    If one file has include the code which you want to insert (You can see a value of the variable which named ```headDuplicaetRule``` in pop-insertCode.py),program will not changed this file,and create a record in  log...
    
  3).```duplicate-more``` log:
    If one file include another more code which you want to insert(This is possible that some one may had inserted the code in some files before .),program will not chaged this file,and create a record in log...
    
  4).```error``` log:
    Some error occures When program is running ,this error will be record into this log.
    
  5).```ignore``` log:
    Files which are out of your filter rule will be record into this log.
    
  6).```no-change``` log:
    FIles which include into your filter rule but have no someplace to insert your code will be record into this log.
    
  7).```warn``` log:
  
  
  
  --------Because of my daily work,English document will be continued latter,please wait for days....or you can mail me...
  
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
  python pop-insertcode.py /Users/ashihiroshi/Downloads/buyerInfoSearch/
  ```
  
  第一个参数是python的启用脚本语句，第二个参数是执行该脚本，第三个参数是需要插入代码的目录的路径。程序将会对 ```sh/Users/ashihiroshi/Downloads/buyerInfoSearch/ ```
  即，将对buyerInfoSearch目录进行遍历，在此之前会在脚本当前所在页生成 buyerInfoSearch_generator_timestamp 
  为名称的文件夹，同时对buyerInfoSearch的目录进行备份并放在backup文件夹中，所有的生成的文件包括日志和备份都会放在该文件夹内。

  打开pop-insertcode.py脚本，可以根据个性化需要修改的相应参数详述如下：
  	
  filterRule常量：即过滤规则，filterRule是一个数组，表示脚本仅执行filterRule数组中所罗列的文件的扩展名（此处只针对扩展名，不针对具体文件），如果filterRule中没有数据，则将会对所有文件执行遍历
  	
 afterHead:即在head标签下将要添加的代码，如果不希望添加如下链接地址的js脚本代码，可以修改下面的值。
  	
 beforeBody：即在```</body>```标签之前添加相应代码
  	
 headDuplicaetRule:执行判重规则，即如果所述页面存在该值所对应的代码，则不会再进行相应添加，同时会记录相应日志，防止重复添加同样的代码。
  	
 bodyDuplicateRule:作用如headDuplicaetRule
  	

  	#!/usr/bin/env python
  	version="v0.4Beta"

	argv = sys.argv;
	
	#扩展名过滤规则，即，只对.html扩展名的文件进行操作
	#File filter,you can add file type which you need,such as ".vm","jsp" etc...
	filterRule=['.html','.jsp'];
	
	#The code whitch I'll replace in all files;
	afterHead = '<script src="hc.common.js"></script>'
	
	beforeBody = '<script src="hc.control.js"></script>'
	
	#If some files had been insert the same code,these will not be changed again...
	headDuplicateRule='hc.common.js'
	bodyDuplicateRule='hc.control.js'
	

  执行效果如下：
  ```
  |-----------------------------------------------------------------------|
|                PopInsertCode Version: v0.4Beta                        |
|                @Author:Andrew Lee                                     |
|                @Email:lipengfei217@163.com                            |
|                @GitHub:https://github.com/lipengfei217                |
|-----------------------------------------------------------------------|

Caculating quantity of all files,please wait....
-----------------------------------------------------------------------
                 TotalFiles： 12
-----------------------------------------------------------------------
 Now is creating a bakup，please wait for minutes......
tar -czvf buyerInfoSearch_generator20141031163523/backup/buyerInfoSearch_backup20141031163523.tar.gz buyerInfoSearch/


-------------Backup accomplish ,path is /Users/ashihiroshi/Workspaces/pythonSpace/work/userActiveCode/src/buyerInfoSearch_generator20141031163523/backup/buyerInfoSearch_backup20141031163523.tar.gz

Create folder :buyerInfoSearch_generator20141031163523/logs
Create folder :buyerInfoSearch_generator20141031163523/code

Executed Files：12 | Changed Files：8 | Remaining Files：0 | Faild Files：0 | 100%  ||====================================================================================================->

Program Over

  Program Over

```

图中会实时显示执行的进度，具体含义如下所述：
	
  a. Executed Files:当前已经执行过的文件数

  b. Changed Files:当前已经执行过的且符合filterRule过滤规则的文件数，即 Changed Files = 文件总数-到当前为止不符合过滤规则的文件数

  c.Remaining Files:当前剩余的还需要执行的文件

  d.Faild Files:报错的文件数，通常如果执行某个文件时出现脚本错误等，次数将会+1并记录日志。
 
