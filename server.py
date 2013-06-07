import tornado.web
import tornado.ioloop
from tornado.template import Template
from tornado.template import Loader
import sqlite3
import db
from db import BankTable
import random
import sys

def log(str):
    sys.stderr.write(str + "\n")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
	loader = Loader("./");
	bl = db.getAvailableBanks();
	self.write(loader.load("index.html").generate(availableBanks=bl));

class TableHandler(tornado.web.RequestHandler):
    def get(self):
	loader = Loader("./");
        bankName = self.get_argument("bank_name");
	bl = db.getBankList(name = bankName);
	self.write(loader.load("table.html").generate(banks=bl));

class CheckHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument("id");
        op = self.get_argument("op");
        if op == "accept":
            opFlag = BankTable.FLAG_ACCEPT;
        elif op == "unaccept":
            opFlag = BankTable.FLAG_UNACCEPT;
        else:
            opFlag = BankTable.FLAG_POSTPONE;
        db.checkProm(id, opFlag);

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/assets/css/(.*)", tornado.web.StaticFileHandler, {"path": "./assets/css/"}),
    (r"/assets/js/(.*)", tornado.web.StaticFileHandler, {"path": "./assets/js/"}),
    (r"/assets/img/(.*)", tornado.web.StaticFileHandler, {"path": "./assets/img/"}),
    (r"/table.html", TableHandler),
    (r"/check.py", CheckHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
    ]);

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
