import urllib
from util import log
from bs4 import BeautifulSoup

class BaseGetter:
    MAX_PAGE_COUNT = 2000;
    TEST_PAGE_COUNT = 4;

    def openUrl(self, url):
        f = urllib.urlopen(url);
	if f.getcode() != 200:
	    return None;
	else:
	    return f;
    
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
