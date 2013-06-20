import urllib
import urllib2
from util import log
from bs4 import BeautifulSoup
import settings
import sys

class BaseGetter:
    MAX_PAGE_COUNT = 20000;
    TEST_PAGE_COUNT = 4;

    def openUrl(self, url):

	if settings.MODE_DEBUG:
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

    def getSoup(self, url):
       f = self.openUrl(url); 
       if f == None:
           return None;
       else:
           return BeautifulSoup(f);
    
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
	    return 2;
	else:
	    return MAX_PAGE_COUNT;
