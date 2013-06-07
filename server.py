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

        bl = db.getBankList(whereDict);
	self.write(loader.load("table.html").generate(banks=bl));

class CheckHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument("id");
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
