# -*- coding: utf-8 -*-

import urllib, urllib2, re, sys,csv
import numpy as np
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

class myparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.isNumber = 0
        self.numbers = []
        
    
    def handle_starttag(self, tag, attrs):
        if tag == 'span' and attrs == [('class','hl f1')]: # identify >99
            # f1 = red / f2 = green / f3 = yellow
            self.isNumber = 1
        elif tag == 'div' and attrs == [('class','title')] and self.isNumber == 1: # marker
            self.isNumber = 2
            
        elif tag == 'a' and self.isNumber == 2: # identify hyper link and add it into list
            self.numbers.append(attrs[0][1])
            
        elif tag == 'span' and attrs != [('class','hl f1')]:
            self.isNumber = 0
        
            #print "Encountered a start tag:", tag
    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        return
    def handle_data(self, data): # handling the data
        if self.isNumber == 2:
            if '\n' in data:
                pass
            else:
                self.numbers.append(data)
                
        
            
            #print "Encountered some data  :", data

KeyFile = open('KeywordFile.txt','r')
items = KeyFile.readlines()
KeyFile.close()
rec = 0 # initalize number recorder
#data = np.array # initalize numpy array
f = file('Output.csv','ab')

print items
for i in range(len(items)):
    items[i] = (unicode(items[i]).encode('utf-8') + '\r')

for j in range(len(items)):
    
    keyword = items[j]
    #keyword_dec = urllib.quote(keyword.encode('utf-8'))
    keyword_dec = urllib.quote(keyword)
    yahooPageCode = '&xargs=12KPjg1oduy5a3vOHvKvjFTfXBhg9O0JC35Is_WMQaRp8L_XNrR6AuOfa_3pgqGK5q7C_g_Q%2E%2E&pstart=5&b='
    #yahooPageNum = range(1,100,10)
    for yahooPageNum in range(1,50,10):
    #yahooPageNum = 11
        URL = 'http://tw.news.search.yahoo.com/search?p=' + keyword_dec + yahooPageCode + str(yahooPageNum)
        #URL = 'http://www.cna.com.tw/search/hysearchws.aspx?q=' + urllib.parse.quote(keyword)
        print(URL)

        response = urllib.urlopen(URL)
        soup = BeautifulSoup(response)
        
        x = soup.find_all("div",{"class" : "res"})
        for i in range(len(x)):
            if 'sc' in x[i].attrs.values()[0]:
                pass
            else:
                Title = x[i].find('a').text; URN = x[i].find('a').get('href'); Source = x[i].find("span",{"class" : "url"}).text; Time = x[i].find("span",{"class" : "timestamp"}).text
                #print Title
                #print URN
                #print Source
                #print Time
                
                data = [Title,URN,Source,Time]
                csv_writer = csv.writer(f,dialect='excel')
                csv_writer.writerow(data)
                
                                
                
                #print '-------'
                rec += 1
                
                

print ' --- End -----'
print rec
f.close()