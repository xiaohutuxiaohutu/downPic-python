import requests
from bs4 import BeautifulSoup
import os
import sys
import imghdr
import time
import io
import re
import datetime
import random
from urllib.request import Request
from urllib.request import urlopen
if(os.name=='nt'):
    print(u'windows 系统')
else:
    print(u'linux')

proxyipurl='http://www.xicidaili.com/'
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
ISOTIMEFORMAT='%Y-%m-%d %X'

#获取代理IP
def get_ip_list(proxyipurl):
    request = Request(proxyipurl, headers=header)
    response = urlopen(request)
    obj = BeautifulSoup(response, 'lxml')
    ip_text = obj.findAll('tr', {'class': 'odd'})
    ip_list = []
    for i in range(len(ip_text)):
        ip_tag = ip_text[i].findAll('td')
        ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text()
        ip_list.append(ip_port)
    #检测IP是否可用   
    for ip in ip_list:
        try:
            proxy_host='https://'+ip   
            proxy_temp={"https:":proxy_host}    
            res=urllib.urlopen(url,proxies=proxy_temp).read()
        except Exception as e:         
            ip_list.remove(ip)
            continue
    return ip_list
#从IPlist中获取随机地址
def get_random_ip(ip_list):
    #ip_list = get_ip_list(bsObj)
    random_ip = 'http://' + random.choice(ip_list)
    proxy_ip = {'http:':random_ip}
    return proxy_ip

file=open("zipai_2018-09-01_3.txt")
ip_list=get_ip_list(proxyipurl)
#获取总行数
for num,value in enumerate(file,1):
    print('第'+str(num)+'行：')
    line=value.strip('\n')
    print(line)
    #获取代理服务器
    proxyip=get_random_ip(ip_list)
    print('proxyip:'+str(proxyip))

    html=requests.get(line,headers = header, proxies=proxyip)
    html.encoding='utf-8'
    itemSoup=BeautifulSoup(html.text,'lxml')
    title=itemSoup.title.string
    title=re.sub(r'<+|>+|/+|‘+|’+|\?+|\|+|"+|\*+|\:+|\【+|\】+','',title)
    print(title)
    imgUrls=itemSoup.select("body div[class='main'] div[class='contentList'] div[class='content'] p img")
    print('图片数量：'+str(len(imgUrls)))
    #print(imgUrls)
    path='E:/图片/zipai/'+datetime.datetime.now().strftime('%Y-%m-%d')+'/'+title+'/'
    for i in range(0,len(imgUrls)):
        fileUrl=imgUrls[i].get('src')
        image_name=fileUrl.split("/")[-1]
        print('开始下载-第%i个：%s'%(i+1,fileUrl))
        #imageUrl=requests.get(fileUrl,headers=header,proxies=proxyip,timeout=None)
        bl=True
        while bl:
            try:
                imageUrl=requests.get(fileUrl,headers=header,proxies=proxyip,timeout=None)
                #print(imageUrl.status_code)
                if imageUrl.status_code==200:
                    bl=False
                    if not(os.path.exists(path)):
                        os.makedirs(path)
                    os.chdir(path)
                    f=open(image_name,'wb')
                    f.write(imageUrl.content)
                    f.close()
            except requests.exceptions.RequestException:
                print('--第%i：---%s连接错误----'%(i+1,fileUrl))
                #print('错误码：'+str(imageUrl.status_code))
    print("-----down over----------------")
file.close
print("all over")
