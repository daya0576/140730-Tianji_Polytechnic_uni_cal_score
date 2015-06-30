# -*- coding: utf-8 -*- 
import urllib, urllib2, cookielib, sys, time, os
from bs4 import BeautifulSoup 
import chardet
import types  

print '''@author: cs1104 zcj ^_^'''
print '''@version:ver1.1'''
print '''-----------input----------------'''
passwd = "***"
name = "***"
choise = "***"
requered_only = False
name = sys.argv[1]
passwd = sys.argv[2]

'''
print unicode("学号：","utf8")
name = raw_input(unicode(" id:","utf8"))
print unicode("密码：","utf8")
passwd = raw_input(unicode(" passwd: ","utf8"))
'''

#print unicode(" 只计算必修的课？：","utf8")
#chiose = raw_input(unicode("required classes only?(yes/no):","utf8"))
# if "y" in chiose:
#     requered_only = True
# elif "n" in chiose:
#     requered_only = False
# else:
#     print "。。。yes or no, this is a question "


print '''--------------------------------'''

def main_is_frozen():
    """Return ''True'' if we're running from a frozen program."""
    import imp
    return (
        # new py2exe
        hasattr(sys, "frozen") or
        # tools/freeze
        imp.is_frozen("__main__"))
 
def get_main_dir():
    """Return the script directory - whether we're frozen or not."""
    if main_is_frozen():
        return os.path.abspath(os.path.dirname(sys.executable))
    return os.path.abspath(os.path.dirname(sys.argv[0]))

def write_to_file(filename, str):
    file_object = open(filename, 'w')
    try:
        file_object.write(str)
    finally:
        file_object.close()

def get_date(score_content):
    soup = BeautifulSoup(score_content)
    table_all = soup.find_all('table', class_ = "titleTop2" )
    title_all = soup.findAll("b")
    
    titles = []
    for tab_b in title_all:
        #print type(tab_b.text)
        
        title = tab_b.text.strip()
        titles.append(str(title))
    
    table_score_all = []
    for i, tables in enumerate(table_all):
        table = tables.find('table')
        rows = table.findAll('tr')
        
        lines=[]
        for tr in rows:
            cols = tr.findAll('td')
            line = []
            for td in cols:
                if td.find('p') != None:
                    text = td.find('p').text.strip()
                else:
                    text = td.text.strip()

                line.append(str(text))
            
            lines.append(line)
        
        table_score_all.append([titles[i], lines])
        
    return table_score_all

def get_context(table_score_all):
    text = ""
    term_sum = len(table_score_all)
    score_term_sum = []
    weight_term_sum = []
    for i in range(term_sum):
        score_term_sum.append(0.0)
        weight_term_sum.append(0)
    
    for term_num, term in enumerate(table_score_all):
        title = term[0]
        text = text + title + "\n"
        
        subjects = term[1]
        for subject in subjects:
            if len(subject) == 7:
                if "双学位" in subject[2]:
                    continue
                if "通过" in subject[6]:
                    continue
                if requered_only:
                    if "任选" in subject[5]:
                        continue
                    text = text + "%-40s%20s%20s%20s"%(subject[2],subject[4],subject[5],subject[6]) + '\n'
                    score_term_sum[term_num] += float(subject[6]) * int(subject[4])
                    weight_term_sum[term_num] += int(subject[4])
                else:
                    text = text + "%-40s%20s%20s%20s"%(subject[2],subject[4],subject[5],subject[6]) + '\n'
                    score_term_sum[term_num] += float(subject[6]) * int(subject[4])
                    weight_term_sum[term_num] += int(subject[4])
            else:
                pass
            #print "\n"
            
        if weight_term_sum[term_num] != 0:
            text += "score_term_average: " + str(float(score_term_sum[term_num]) / weight_term_sum[term_num]) + '\n'
            text += "weight_term_sum: " + str(weight_term_sum[term_num]) + '\n'
            text += '\n'

    final_average = 0
    score_sum = 0
    weight_sum = 0
    for (score, weight) in zip(score_term_sum, weight_term_sum):
        score_sum += score
        weight_sum += weight
    
    if score_sum != 0:    
        final_average = float(score_sum) / weight_sum
        text += "\n"+"final_average: " + str(final_average)
    
    return text

class Score_info(object):
    def __init__(self , name = "*******" ,passwd='******',):
        self.username = int(name)
        self.password = int(passwd)
        self.posturl = 'http://jwpt.tjpu.edu.cn:8081/loginAction.do'   
        self.header = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        
        self.postData_temp = urllib.urlencode({'zjh':name, 'mm':passwd})
        
        cj = cookielib.LWPCookieJar()  
        cookie_support = urllib2.HTTPCookieProcessor(cj)  
        self.opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

                
    def login(self):
        req = urllib2.Request(self.posturl, self.postData_temp, self.header)
        resp = self.opener.open(req)  
        result = resp.read()
        
        if '/menu/s_top.jsp' in result:
            flag_login = True
            print "logining success"
            print "waiting..."
        else:
            flag_login = False
            print "logining wrong~"
            print "check your id and passwd"
            exit()

        return flag_login
    
    def get_score(self):
        #req = urllib2.Request('http://jwpt.tjpu.edu.cn:8081/gradeLnAllAction.do?type=ln&oper=qb', None, self.header)
        req = urllib2.Request('http://jwpt.tjpu.edu.cn:8081/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2013-2014%E5%AD%A6%E5%B9%B4%E6%98%A5(%E4%B8%A4%E5%AD%A6%E6%9C%9F)#qb_2013-2014学年春(两学期)', None, self.header)
        resp = self.opener.open(req)
        score_content = resp.read()
        
        if os.path.exists("result"):  
            pass  
        else:  
            os.mkdir("result")
        write_to_file(get_main_dir() + "/result/result.html", score_content)
        #统一编码格式
        charset = chardet.detect(score_content)
        charset = charset['encoding']
        if charset !='utf-8' and charset !='UTF-8':
            scorePage = score_content.decode('gbk' , 'ignore').encode("utf-8")
        unicodePage = scorePage.decode('utf-8')
        
        return scorePage




'''login'''
daya_score = Score_info(name, passwd)
daya_score.login()  
score_content = daya_score.get_score() 

'''解析html'''
table_score_all = get_date(score_content)
print "calculating..."
text = get_context(table_score_all)


write_to_file(get_main_dir() + "/result/result.txt", text)

print "succeed! open result.txt in your \"result\" folder~"
print unicode("完成。打开目录下的result文件夹 ","utf8")

time.sleep(5)


