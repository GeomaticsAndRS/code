#!/bin/env python

import json
import urllib2
import smtplib
from email.mime.text import MIMEText
from email.header import Header

url="http://2.1.1.2/status?format=json"

class GET_DATA:
    """
    get the status data
    """

    def __init__(self):
        """
        init 
        """
        self.user_aget = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent':'self.user_agent'}

    def req_data(self):
        """
        get the data from here
        """
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            web_page = response.read()
            return web_page
        except urllib2.URLError,e:
            print u'open url error',e.reason
            return None 

class ANALYZE_DATA:
    """
    """
    def __init__self(self):
        ""
        ""

    def get_down(self,json_to_dict):
        """
        """
        result = ''
        cc = []
        data = json_to_dict
        data_list = data['servers']['server']
        for i in range(len(data_list)):
            if data_list[i]['status'] == 'down':
                aa = [data_list[i]['upstream'],data_list[i]['name'],data_list[i]['status']]
                bb = " ".join(aa)
                cc.append(bb)
        result = "\n".join(cc)
        return result

class MYMAIL:
    """
    """
    def __init__(self):
        self.mail_user = "@qq.com"
        self.mail_passwd = ""
        self.mail_to = "@qq.com"
        self.mail_from = "@qq.com"

    def sendmail(self,message):
        """
        """
        msg = MIMEText(message,'plain','utf-8')
        msg['From'] = Header("Monitor ","utf-8")
        msg['To'] = Header("Devopt",'utf-8')
        msg['Subject'] = Header('Nginx Monitor','utf8')

        try:
            smtpObj = smtplib.SMTP_SSL('smtp.qq.com','465')
            smtpObj.connect('smtp.qq.com',465)
            smtpObj.login(self.mail_user,self.mail_passwd)
            smtpObj.sendmail(self.mail_from,self.mail_to,msg.as_string())
            smtpObj.close() 
            return True
        except smtplib.SMTPException,e:
            print str(e)
            return False

def main():
    """
    """
    get_data = GET_DATA()
    analyze = ANALYZE_DATA()
    mail = MYMAIL()
    source_data = get_data.req_data()
    json_to_dict = json.loads(source_data)
    dict_data = analyze.get_down(json_to_dict)
    print dict_data
    ok = mail.sendmail(dict_data)
    if ok:
        print "send ok"

if __name__ == '__main__':
    main()
