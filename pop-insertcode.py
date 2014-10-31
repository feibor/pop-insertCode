#!/usr/bin/env python
# coding=utf-8
#Author:
#Date:2014-10-22
#email:lipengfei217@163.com | lipengfei02@hc360.com

import os
import sys
import thread
import time
import commands
import re
import traceback

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


###Generator the main foloder name.
###Main folder will be generatored in which pop-insertcode.py be runned...

dir_suffix = '_generator'+time.strftime('%Y%m%d%H%M%S');
###


###Get currentPath ..
currentRootPath=os.getcwd();



totalFiles = 0;
faildFiles=0;


#修改的文件数
changedFiles=0;

currentProcess= 0;


#To back up your work dir before program
def doBak():
  #Str
  #ifBackup = raw_input("---------Do you want to backup your files?Y/n---------\n");
  ifBackup = "y";

  #转换成小写,即，使用户的输入忽略大小写
  #None case sensitive...
  ifBackup = ifBackup.lower();

  backupFileName= getFolderName(argv[1])+'_backup'+time.strftime('%Y%m%d%H%M%S')+'.tar.gz';

  if str(ifBackup)=='y':

      commands.getstatusoutput('mkdir -p '+filesMkdir+'/backup');

      print " Now is creating a bakup，please wait for minutes......"

      tarCommand = 'tar -czvf '+filesMkdir+'/backup/'+backupFileName+' '+argv[1];

      print tarCommand;

      status,ref = commands.getstatusoutput(tarCommand);

      if(status==0):
          #print ref;
          print '\n';
          print '-------------Backup accomplish ,path is '+os.getcwd()+'/'+filesMkdir+'/backup/'+backupFileName+'\n'

      else:
          s = raw_input("---------Back up coming up an error ,do you want to continue(you will have no backup)？Y/n---------:\n");
          s = s.lower();
          if str(s)!='y':
              exit();

def getFolderName(path):
  array = path.split("/");
  length = len(array);

  if(length>1):

    for i in reversed(range(0,length)):
      if array[i]:
        return array[i];
  elif length==0:
    return array[0];


def mkdirs():

    doBak();

    print "Create folder :"+filesMkdir+'/logs';
    mkdirStatus,mkdir = commands.getstatusoutput('mkdir -p '+filesMkdir+'/logs');

    print "Create folder :"+filesMkdir+'/code';
    mkdirStatus1,mkdir1 = commands.getstatusoutput('mkdir -p '+filesMkdir);

    if(mkdirStatus==0 and mkdirStatus1==0):
        print mkdir;
    else:
        print"You got an error when create a folder!Program will exit！";
        exit();



def analyEngineThread():
    global currentProcess;
    while totalFiles>currentProcess:
        time.sleep(1);
        walk_dir(argv[1]);
        #currentProcess+=1;
    thread.exit_thread()



#reStr:正则表达式;
#context:需要查找的内容
def searchEngine(reStr,context):
    code_re = re.compile(reStr,re.I);
    strSearch = code_re.search(context);
    return strSearch;

def findEngine(reStr,context):
    code_re = re.compile(reStr,re.I);
    allArry = code_re.findall(context);
    return allArry;

def replaceEngine(reStr,replaceContext,context):
    code_re = re.compile(reStr,re.I);
    resultStr = code_re.sub(replaceContext,context);
    return resultStr;

def doInsert(fromPath,toPath,fileName):
    global filterRule;
    global changedFiles;

    try:

        replace_re1 =r'<\s*\bhead\b[^>]*>';

        replace_re2 = r'</(\bbody\b)[^>]*>';

        #建立相应目录
        #Create relationable dirs...
        commands.getstatusoutput('mkdir -p '+toPath);

        #filePath = fromPath+'/'+fileName;
        filePath = os.path.join(fromPath,fileName);
        newFilePathName =toPath+'/'+fileName;
        currentFile = open(filePath,'r');
        content = currentFile.read();


        #打开各个文件------START----
        #Create a lot logs...

        currentTime = time.strftime('%Y-%m-%d');


        logFile_nochange = open(filesMkdir+'/logs/nochange-'+currentTime+'.log','a');
        f = open(newFilePathName,'a');
        logFile_info = open(filesMkdir+'/logs/info-'+currentTime+'.log','a')
        logFile_error = open(filesMkdir+'/logs/error-'+currentTime+'.log','a')
        logFile_ignore = open(filesMkdir+'/logs/ignore-'+currentTime+'.log','a')
        logFile_infoDetail = open(filesMkdir+'/logs/detail-'+currentTime+'.log','a')
        logFile_warn = open(filesMkdir+'/logs/warn-'+currentTime+'.log','a')
        logFile_duplicate = open(filesMkdir+'/logs/duplicate-'+currentTime+'.log','a')
        logFile_duplicateMore = open(filesMkdir+'/logs/duplicate-more-'+currentTime+'.log','a')

        #打开各个文件------END-----


        #得到文件的扩展名

        extendName = os.path.splitext(fileName)[1];

        ifIgnore = True;

        #如果未添加过滤规则，则不进行任何过滤，否则需要进行过滤规则处理
        if len(filterRule)>=0:
            if len(filterRule)==0:
                ifIgnore=False;
            else:
                for fl in filterRule:=
                    if(extendName==fl):
                        ifIgnore=False;


        if ifIgnore:
            commands.getstatusoutput('cp '+filePath+" "+newFilePathName);
            logFile_ignore.write(newFilePathName+'[Time:'+time.strftime('%Y-%m-%d %H:%M:%S')+']\n');
            return;

        #及时关掉文件，只操作content部分即可

        changedFiles+=1;

        currentFile.close();



        ###------ Main code start --------

        ### Because I have tow part code to insert,so I have to do two regular expression to insert my code...
        ### If you only have one part to insert,you can delete one variable...

        searchCode1 = searchEngine(replace_re1,content);

        searchCode2 = searchEngine(replace_re2,content);


        headCheckDuplicate = searchEngine(headDuplicateRule,content);

        bodyCheckDuplicate = searchEngine(bodyDuplicateRule,content);

        #-----more of same code in one files....
        headCheckDuplicateMore = findEngine(headDuplicateRule,content);
        bodyCheckDuplicateMore = findEngine(bodyDuplicateRule,content);


        check1 = findEngine(replace_re1,content);
        check2 = findEngine(replace_re2,content);

        if len(headCheckDuplicateMore)>1:
          logFile_duplicateMore.write(newFilePathName+' contains multiply code:'+headDuplicateRule+' [Time:'+time.strftime('%Y-%m-%d %H:%M:%S')+']\n');

        if len(bodyCheckDuplicateMore)>1:
          logFile_duplicateMore.write(newFilePathName+' contains multiply code:'+bodyDuplicateRule+' [Time:'+time.strftime('%Y-%m-%d %H:%M:%S')+']\n');

        if len(check1)>1 :
            logFile_warn.write(newFilePathName+' contains multiply head tag [Time:'+time.strftime('%Y-%m-%d %H:%M:%S')+']\n');

        if len(check2)>1 :
            logFile_warn.write(newFilePathName+' contains multiply body tag [Time:'+time.strftime('%Y-%m-%d %H:%M:%S')+']\n');

        info = content;
        logsInfo="";
        replaceStr1="";
        #在head标签后面插入第一个脚本

        if searchCode1:
          #No duplicate code ,will be insert..
          if not headCheckDuplicate:

              replaceStr1 = searchCode1.group();
              replaceStr1 +="\n"
              replaceStr1+=afterHead+'\n';

              #info = code_re1.sub(replaceStr1,content);

              info = replaceEngine(replace_re1,replaceStr1,content)

              logsInfo = newFilePathName+":"+searchCode1.group()+"=======>\n"+replaceStr1+'\n[Time:'+time.strftime('%Y-%m-%d %H:%M:%S')+']\n'

          else:
              duplicateWarningInfo = headDuplicateRule+":"+newFilePathName
              logFile_duplicate.write(duplicateWarningInfo+"\n");

        else:

            info = content;

        if searchCode2:
          if not bodyCheckDuplicate:

            replaceStr2 = searchCode2.group();
            replaceStr="";
            replaceStr+=beforeBody+"\n"+replaceStr2;
            info = replaceEngine(replace_re2,replaceStr,info);

            if searchCode1:
                logsInfo = newFilePathName+":"+searchCode1.group()+"=======>\n"+replaceStr1+'\n'+"---------Split-----------\n"+searchCode2.group()+"=======>\n"+replaceStr+'[Time:'+time.strftime('%Y-%m-%d %H:%M:%S')+']\n'
            else:
                logsInfo = newFilePathName+":"+searchCode2.group()+"=======>\n"+replaceStr+'\n[执行时间:'+time.strftime('%Y-%m-%d %H:%M:%S')+']\n'
          else:
            duplicateWarningInfo = bodyDuplicateRule+":"+newFilePathName
            logFile_duplicate.write(duplicateWarningInfo+"\n");
        else:
            if not searchCode1:
                #logsNochange = newFilePathName+":"+"无变化"+'[执行时间:'+time.strftime('%Y-%m-%d %H:%M:%S')+']\n'
                logsInfo="";
                nochangeLogoInfo = newFilePathName+"\n";
                logFile_nochange.write(newFilePathName+"\n");
                info = content;


        #在</body>标签之前插入

        f.write(info);


        logFile_info.write(newFilePathName+'[Time:'+time.strftime('%Y-%m-%d %H:%M:%S')+']\n');
        logFile_infoDetail.write(logsInfo);

    except:
        global faildFiles;
        faildFiles+=1
        errorStr = newFilePathName+'get an error!';
        logFile_error.write(errorStr);
        traceback.print_exc(file=logFile_error);
        logFile_error.write('[Time:'+time.strftime('%Y-%m-%d %H:%M:%S')+']\n');

    finally:

        if f:
            f.close();

        if logFile_info:
            logFile_info.close();

        if logFile_nochange:
            logFile_nochange.close();

        if logFile_error:
            logFile_error.close();

        if logFile_ignore:
            logFile_ignore.close();

        if logFile_infoDetail:
            logFile_infoDetail.close();

        if logFile_warn:
            logFile_warn.close();

        if logFile_duplicate:
            logFile_duplicate.close();


        if logFile_duplicateMore:
            logFile_duplicateMore.close();




#Loop dirs ...
def walk_dir(dirPath,topdown=True):

    #Having been done's files' quantity
    global currentProcess;

    equalDir = "";
    for root, dirs, files in os.walk(dirPath, topdown):

        #equalDir =os.path.join(equalDir,getFolderName(root));

        #print equalDir;

        #toPathDir=os.path.join(currentRootPath,name);

        #print os.path.join(root,filesMkdir,currentRootPath);

        toPathDir = root.replace(dirPath,os.path.join(currentRootPath,filesMkdir,getFolderName(argv[1])+"/"));

        for name in files:



            #print getFolderName(root)+"-----------";
            #print currentRootPath+"------------------"+filesMkdir+"-----------"+getFolderName(root)+"-----------"+name;

            doInsert(root,toPathDir,name);

            #doInsert(os.path.join(os.getcwd(),root),os.path.join(root,filesMkdir,currentRootPath),name);
            #doInsert(os.path.join(os.getcwd(),root),toPathDir,name);
            #toPath =  os.path.join(root,filesMkdir,currentRootPath);
            #print os.path.join(os.getcwd(),root,name)+"========>"+os.path.join(currentRootPath,filesMkdir,root);
            #print toPath+'/'+name;
            #print os.path.join(root,name);
            #print dirPath;
            #print root+"------------"+dirPath+"-------------"+root.replace(dirPath,os.path.join(currentRootPath,filesMkdir,getFolderName(argv[1])+"/"));
            #print root;
            currentProcess+=1;




#执行主线程之前需要做的操作，如打印，得到总文件数等
#Do print and any other print action...
def beforeThread():

  global filesMkdir
  global dir_suffix;

  if(len(argv)>1):



    #Get the quantity of all files...
    global totalFiles;

    filesMkdir=getFolderName(argv[1])+dir_suffix;

    if not os.path.isdir(argv[1]):
      print "-----------------------------------------------------------------------"
      print "                 Error!Work folders cannot be fund!                    "
      print "-----------------------------------------------------------------------"
      exit();


    #print filesMkdir;

    #exit();


    #得到该文件夹下的文件总数目
    totalFiles  = sum([len(files) for root,dirs,files in os.walk(argv[1])])

    print "Caculating quantity of all files,please wait...."

    print "-----------------------------------------------------------------------"
    print "                 TotalFiles：",totalFiles
    print "-----------------------------------------------------------------------"

    mkdirs();

  else:
      print "\n"
      print "-----------------------------------------------------------------------"
      print "                 Error:Please indicate a folder！"
      print "-----------------------------------------------------------------------"
      exit();








#Print waiting string ...
def progressPrint(character="=",end=False):
  global currentProcess;
  global totalFiles;
  global faildFiles;
  global changedFiles;


  fPrograss = 100.0 * currentProcess/totalFiles;



  if not end:
    j = getNumProgress(character,int(fPrograss));
    printStr = 'Executed Files：'+str(int(currentProcess))+' | Changed Files：'+str(int(changedFiles))+' | Remaining Files：'+str(int(totalFiles-currentProcess))+' | Faild Files：'+str(int(faildFiles))+" | " +str(int(fPrograss))+'%  ||'+j+'->'+"\r"
  else:
    j = getNumProgress(character,int(100));
    printStr = 'Executed Files：'+str(int(totalFiles))+' | Changed Files ：'+str(int(changedFiles))+' | Faild Files：'+str(int(faildFiles))+" | " +str(int(100))+'%  ||'+j+'->'+"\r" ;

  return printStr;


def getNumProgress(character,num):
  printStr="";
  #printChra = str(character);
  for i in range(0,num):
    printStr+="=";
  return printStr;


##Start a thread and record progress...
def startProgress():

            global currentProcess;
            global totalFiles;
            global faildFiles;
            global changedFiles;

            print "|-----------------------------------------------------------------------|"
            print "|                PopInsertCode Version:",version,"                       |"
            print "|                @Author:Andrew Lee                                     |"
            print "|                @Email:lipengfei217@163.com                            |"
            print "|                @GitHub:https://github.com/lipengfei217                |"
            print "|-----------------------------------------------------------------------|\n\n\n"

        #if(len(argv)>1):

            #Do print and any other print action...
            beforeThread();

            #Do main thread
            thread.start_new_thread(analyEngineThread,())

          #Do loop to print progress ...
            while True:
                time.sleep(0.5)
                printStr = progressPrint();

                sys.stdout.write(printStr);
                sys.stdout.flush()
                if totalFiles <= currentProcess:
                    sys.stdout.flush();
                    printStr = progressPrint(True);
                    sys.stdout.write(printStr);
                    break;
            sys.stdout.flush()
            print"\n"
            print "Program Over"
        #else:
            #print "\n"
            #print "-----------------------------------------------------------------------"
            #print "                 Error:Please indicate a folder！"
            #print "-----------------------------------------------------------------------"
            #exit();


if __name__ == '__main__':

    startProgress();

    print """
    Program Over
    """
