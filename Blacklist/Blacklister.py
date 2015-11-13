#!/usr/bin/env python3

import atexit
import subprocess
from bs4 import BeautifulSoup as sop
import urllib.request as reqa
global user_agent,headers
import argparse
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
headers = { 'User-Agent' : user_agent }
parser = argparse.ArgumentParser()
parser.add_argument("countries",type=str, nargs='+',help="The countires to be blacklisted (Codes only)")
args = parser.parse_args()

def getpage(url):
    req = reqa.Request(url,None, headers)
    res = reqa.urlopen(req)
    page = res.read()
    return page

def getcon(url):
    global headers
    li = []
    page = getpage(url)
    soup = sop(page,"html.parser")
    tds = soup('td')
    for content in tds:
        if content.a:
            txt = content.a.text
            if txt != '':
                li.append(txt)
    return li

blist = open('blacklist.txt','w')
def exi():
    global blist
    if blist:
        blist.flush()
        blist.close()

atexit.register(exi)

def whois(asn):
        whois_str =  "whois -h whois.radb.net -- '-i origin "+asn+"' | grep -Eo \"([0-9.]+){4}/[0-9]*|([0-9A-Fa-f:]+)+/[0-9]*\""
        subprocess.call(whois_str,shell=True,stdout = blist)
allasns = []
for x in args.countries:
    allasns += getcon('http://bgp.he.net/country/{}'.format(x))

for asn in allasns:
    whois(asn)

