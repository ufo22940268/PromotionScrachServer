import tornado.web
import tornado.ioloop
from tornado.template import Template
from tornado.template import Loader
import sqlite3
import db
from db import BankTable
import random
import sys
from util import log
import util
import settings

class MainHandler(tornado.web.RequestHandler):
    def get(self):
	loader = Loader("./");
	bl = db.getAvailableBanks();
	self.write(loader.load("index.html").generate(availableBanks=bl));

class TableHandler(tornado.web.RequestHandler):
    def get(self):
	loader = Loader("./");
        bankName = self.get_argument("bank_name");
        state = self.get_argument("state");
        page = int(self.get_argument("page", "1"));
        city = self.get_argument("city", "all");
        whereDict = dict();

        if bankName != "all":
            whereDict[BankTable.COL_NAME] = bankName;
        
        if state == "all":
            pass
        elif state == "accepted":
            whereDict[BankTable.COL_ACCEPTED] = BankTable.FLAG_ACCEPTED;
        elif state == "unaccepted":
            whereDict[BankTable.COL_ACCEPTED] = BankTable.FLAG_UNACCEPTED;
        else:
            whereDict[BankTable.COL_ACCEPTED] = BankTable.FLAG_POSTPONED;

        allBanks = db.getBankList(whereDict, city);
	if self.get_argument("isOption", "false") == "true":
	    cities = self.extractCities(db.getBankList(whereDict));
	    self.write(loader.load("option.html").generate(activedCity=city, cities=cities));
	    return;

        banks = allBanks[(page - 1)*settings.PAGE_COUNT: page*settings.PAGE_COUNT];
        pageCount = len(allBanks)/settings.PAGE_COUNT;
        if pageCount*settings.PAGE_COUNT < len(allBanks):
            pageCount += 1;
        
        pages = self.buildPages(page, pageCount);
	self.write(loader.load("table.html").generate(banks=banks, pages=pages, activePage=page, pageCount=pageCount));

    def buildPages(self, activePage, pageCount):
        pages = [];
        if pageCount <= 9:
            for p in range(1, pageCount + 1):
                pages.append(self.buildPage(activePage, pageCount, p));
            return pages;
        else:
            ns = [activePage,];
            delta = 1;
            while True:
                if 1 < activePage + delta < pageCount:
                    ns.append(activePage + delta);
                    if len(ns) == 7:
                        break;

                if 1 < activePage - delta < pageCount:
                    ns.insert(0, activePage - delta);
                    if len(ns) == 7:
                        break;

                delta += 1;
            if 1 not in ns:
                ns.insert(0, 1);
            if pageCount not in ns:
                ns.append(pageCount);

            for p in ns:
                pages.append(self.buildPage(activePage, pageCount, p));
            return pages;

                    
    
    def buildPage(self, activePage, pageCount, p):
        page = dict();
        page["text"] = str(p);
        if p == 1 and activePage - 1 > 3:
            page["text"] = "... " + page["text"];
        elif p == pageCount and pageCount - activePage > 3: 
            page["text"] = page["text"] + " ...";
        page["value"] = p;
        page["isActive"] = p == activePage;
        return page;

    def extractCities(self, banks):
	cities = set();
	for b in banks:
	    if b.city:
		cities.add(b.city);
	return cities;


class CheckHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument("id", default=None);
        if id == None:
            return;

        op = self.get_argument("op");
        if op == "accept":
            opFlag = BankTable.FLAG_ACCEPTED;
        elif op == "unaccept":
            opFlag = BankTable.FLAG_UNACCEPTED;
        else:
            opFlag = BankTable.FLAG_POSTPONED;
        db.checkProm(id, opFlag);

class UpdateItemStatesHandler(tornado.web.RequestHandler):
    def get(self):
        ids = self.get_argument("ids").split(",");
        acFlag = util.getAcceptedFlag(self.get_argument("op"));
        db.updateItemStates(ids, acFlag);

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/assets/css/(.*)", tornado.web.StaticFileHandler, {"path": "./assets/css/"}),
    (r"/assets/js/(.*)", tornado.web.StaticFileHandler, {"path": "./assets/js/"}),
    (r"/assets/img/(.*)", tornado.web.StaticFileHandler, {"path": "./assets/img/"}),
    (r"/table.html", TableHandler),
    (r"/check.py", CheckHandler),
    (r"/updateItemStates", UpdateItemStatesHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
    ]);

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
