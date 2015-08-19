# coding = utf-8

import re, urllib, urllib2, cookielib, base64, binascii, rsa
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support , urllib2.HTTPHandler)
urllib2.install_opener(opener)

def getData(url) :
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    text = response.read().decode('utf-8')
    return text

def postData(url , data) :
    headers = {'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
    data = urllib.urlencode(data).encode('utf-8')
    request = urllib2.Request(url , data , headers)
    response = urllib2.urlopen(request)
    text = response.read().decode('gbk')
    return text


def login_weibo(nick , pwd) :
    prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.15)&_=1400822309846' % nick
    preLogin = getData(prelogin_url)
    servertime = re.findall('"servertime":(.*?),' , preLogin)[0]
    pubkey = re.findall('"pubkey":"(.*?)",' , preLogin)[0]
    rsakv = re.findall('"rsakv":"(.*?)",' , preLogin)[0]
    nonce = re.findall('"nonce":"(.*?)",' , preLogin)[0]
    su = base64.b64encode(bytes(urllib2.quote(nick) ))
    rsaPublickey = int(pubkey , 16)
    key = rsa.PublicKey(rsaPublickey , 65537)
    message = bytes(str(servertime) + '\t' + str(nonce) + '\n' + str(pwd) )
    sp = binascii.b2a_hex(rsa.encrypt(message , key))
    param = {'entry' : 'weibo' , 'gateway' : 1 , 'from' : '' , 'savestate' : 7 , 'useticket' : 1 , 'pagerefer' : 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D' , 'vsnf' : 1 , 'su' : su , 'service' : 'miniblog' , 'servertime' : servertime , 'nonce' : nonce , 'pwencode' : 'rsa2' , 'rsakv' : rsakv , 'sp' : sp , 'sr' : '1680*1050' ,
             'encoding' : 'UTF-8' , 'prelt' : 961 , 'url' : 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack'}
    s = postData('http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)' , param)
    urll = re.findall("location.replace\(\'(.*?)\'\);" , s)[0]
    getData(urll)
    text = getData('http://www.weibo.com/wangguantong')
    print(text)

# login_weibo('your_account' , 'your_pwd')  
login_weibo('' , '')