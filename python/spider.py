#!/bin/env python
#_*_ coding:utf8 _*_
#This is a script for get jok form the URL which 
#http://cuiqingcai.com/990.html
#This script will send a mail for a mail address,
#after get some jok comtent

#import urllib
import urllib2
import re
import sys
import getopt
import smtplib
from email.mime.text import MIMEText
from email.header import Header

g_debug = 0

class SPIDER:
    """
    spider class will get the jok content and return
    """
  
    def __init__(self):
        """
        this is the spider class init function
        pageIndex : which page will be get
        user_agent : brower type
        enable : whether get
        """
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent':'self.user_agent'}
        self.enable = False
  
    def getPage(self,pageIndex):
        """
        get the web page
        """
        try:
          #url='http://www.qiushibaike.com/text/page/' + str(pageIndex)
          url='http://www.qiushibaike.com/hot/page/' + str(pageIndex)
          request = urllib2.Request(url,headers = self.headers) 
          response = urllib2.urlopen(request)
          pageCode = response.read()
          return pageCode
        except urllib2.URLError,e:
          if hasattr(e,"reason"):
            print u"xxerror reason",e.reason
            return None
  
    def getItems(self,pageIndex):
        """
        analyze and split the jok comtent 
        """
        html="Aha,For Joke:\n"
        for p in range(5):
            html = html + self.getPage(pageIndex) 
        
        pattern = re.compile('<div.*?content">(.*?)</div>',re.S) 
        items = re.findall(pattern,html)
        items = " ".join(items)
        pattern2 = re.compile('<span>(.*?)</span>',re.S)
        items2 = re.findall(pattern2,items)
        return items2

    def start(self):
        """
        start to get jok
        """
        print u"get joke..." 
        self.enable = True
        jokes=self.getItems(2)   
        joke="\n\n\n ".join(jokes)
        ret=joke.replace('<br/>','\n')
        return str(ret)
  

class MYMAIL:
    """
    this class just for send mail 
    """

    def __init__(self):
        """
        set some send mail info 
        mail_user : login user
        mail_passwd : login password
        mail_to : send to 
        mail_from : send from
        """
        self.mail_user = "985695055@qq.com"
        self.mail_passwd = "kgkyggxkxyvpbeih"
        self.mail_to = "2119642367@qq.com"
        self.mail_from = "985695055@qq.com"
    
    def sendmail(self,message):
        """ 
        send a mail for mail_to user
        """ 
        msg = MIMEText(message,'plain','utf-8')
        msg['From'] = Header("msg From ","utf-8")
        msg['To'] = Header("imsg To",'utf-8')
        msg['Subject'] = Header('subject conntt','utf8')
      
        try:
            smtpObj = smtplib.SMTP_SSL('smtp.qq.com','465')
            smtpObj.set_debuglevel(g_debug)
            smtpObj.connect('smtp.qq.com',465)
            smtpObj.login(self.mail_user,self.mail_passwd)
            smtpObj.sendmail(self.mail_from,self.mail_to,msg.as_string())
            smtpObj.close()
        except smtplib.SMTPException,e:
            print str(e)
            return False
        return True 
            

class OTHERS:
    """
    this class own some others info
    """

    def __init__(self):
        """
        nothing to do
        """
        pass 

    def usage(self):
        """
        show a simple userage  and exit
        """
        usage="""
        Usage:
          -h | --help : get the usage page
          -v | --version : get the shell version
          -d | --debug : run the script with debug
          -o | --doc : get a program detail  document info
          -t VALUE | --test VALUE : just for test
        """
        print usage 
        sys.exit()

    def version(self):
        """
        show the version and exit
        """
        version="""
        version-0.2 publish time 2017/02/17
            add OTHERS calss 
        version-0.1 publish time 2017/02/16
            first verson , cat get the jok and send a mail
        """
        print version
        sys.exit()

    def doc(self):
        """
        for this program a detail introduce
        """
        import spider
        print help(spider)
        sys.exit()
 
    def test(self,v):
        """
        just for test
        """
        print "test and value is :",v
        sys.exit()


def main():
    """
    this is a main function ,its the whole run logical for the program
    """

    try:
        opt,args = getopt.getopt(sys.argv[1:],'dhvot:',["debug","help","version","doc","test="])
    except getopt.GetoptError,e:
        print "==>",e

    others = OTHERS()
    for o,v in opt:
        if o in ("-d","--debug"):
            global g_debug
            g_debug = 1
        elif o in ("-h","--help"):
            others.usage()
        elif o in ("-v","--version"):
            others.version()
        elif o in ("-t","--test"):
            others.test(v)
        elif o in ("-o","--doc"):
            others.doc()
        else:
            others.usage()

    spider = SPIDER()
    message = spider.start() 

    mymail = MYMAIL()
    sendStatus = mymail.sendmail(message)

    if sendStatus:
        print "send mail ok"
    else:
        print "send mail fail"

if __name__ == '__main__':
    """
    program start from here
    """
    main()
