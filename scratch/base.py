import urllib
import urllib2
from util import log
from bs4 import BeautifulSoup
import settings
import sys

class BaseGetter:
    def openUrl(self, url):
	#if settings.mode == settings.MODE_DEBUG:
        print url;
        sys.stdout.flush();

        try:
            f = urllib2.urlopen(url);
        except urllib2.HTTPError:
            return None;

	if f.getcode() != 200:
	    return None;
	else:
	    return f;

    def getSoup(self, url, encoding="utf-8"):
       f = self.openUrl(url); 
       if f == None:
           return None;
       else:
           return BeautifulSoup(f, from_encoding=encoding);
    
    def getName(self):
        """docstring for getName"""
        pass

    def fetchBankList(self):
        """docstring for fetchBankList"""
        pass;

    def writeToTest(self, f):
	if f == None:
	    log("file stream is null");
	else:
	    open("test.html", "w").write(f.read());

    def getPageRange(self):
	if settings.mode == settings.MODE_DEBUG:
	    return settings.TEST_PAGE_COUNT;
	else:
	    return settings.MAX_PAGE_COUNT;

    def isSoupEquals(self, s1, s2):
        return s1 and s2 and s1.get_text() == s2.get_text();
