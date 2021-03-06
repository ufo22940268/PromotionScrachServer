import hashlib
from datetime import datetime
from datetime import timedelta

class Bank():
    """docstring for Bank"""
    def __init__(self):
        #These are the only things we need to fetch.
        self.url = "";
        self.title = "";

        #Optional
        self.city = "";
        self.name = "";
        self.fetchTime = "";
	self.accepted = 2;
	self.endDate = None;

    def __str__(self):
        return "url:" + self.url + "\ntitle:" + self.title + "\nendDate:" + str(self.endDate) + "\ncity:" + str(self.city) + "\n\n";

    def hashCode(self):
        urlAndTitle = str(self.url) + str(self.title) + str(self.city);
        m = hashlib.md5();
        m.update(urlAndTitle);
        return m.hexdigest();

    def isExpired(self):
	if not self.endDate:
	    return False;
	else:
	    return (datetime.now() - self.endDate) > timedelta(days=1)

