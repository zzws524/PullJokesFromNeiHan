__author__='ziwen'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import cookielib
import time
import os
import math

class Zspider:
    def __init__(self,jokeQty=32):
        self.url = 'http://neihanshequ.com'
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
        self.stories=[]
        self.storyNum=0
        self.jokeQty=jokeQty

    def GetStory(self):
        try:
            cookie=cookielib.MozillaCookieJar()
            cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
            for i in range(0,5):
                if (len(self.stories)<self.jokeQty):
                    request = urllib2.Request(self.url,headers = self.headers)
                    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
                    response = opener.open(request)
                    content = response.read().decode('utf-8')
                    pattern = re.compile('<h1.*?class="title">.*?<p>(.*?)</p>',re.S)
                    items = re.findall(pattern,content)
                    self.stories=self.stories+items
                    time.sleep(0.5)
                else:
                    break
        except urllib2.URLError as e:
            if hasattr(e,"code"):
                print (e.code)
            if hasattr(e,"reason"):
                print (e.reason)

    def PrintStory(self):
        if os.path.exists('jokes.txt'):
            os.remove('jokes.txt')
        jokeFile=open('jokes.txt','w')
        for eachStory  in self.stories:
            jokeFile.write(str(self.stories.index(eachStory))+eachStory.encode('utf-8')+'\n')
        jokeFile.close()


    def PrepareCookieFile(self):
        if os.path.exists('cookie.txt'):
            os.remove('cookie.txt')
        myFile=open('cookie.txt','w')
        timeStamp= str(math.trunc(time.time()))
        template=['# Netscape HTTP Cookie File\n',
                  '# http://curl.haxx.se/rfc/cookie_spec.html\n',
                  '# This is a generated file!  Do not edit.\n\n',
                  '.neihanshequ.com	TRUE	/	FALSE	'+timeStamp+'	tt_webid	35044269079\n'
                  '.neihanshequ.com	TRUE	/	FALSE	1789641528	uuid	"w:31b374e5e2164794a6b574fde8df36d1"\n'
                  'neihanshequ.com	FALSE	/	FALSE	1510022328	csrftoken	b2b61e34ba5bc026c42873b8025b360c\n']
        myFile.writelines(template)
        myFile.close()

    def Run(self):
        self.PrepareCookieFile()
        self.GetStory()
        self.PrintStory()



if __name__=='__main__':
    mySpider=Zspider()
    mySpider.Run()

