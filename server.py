import tornado.web
import tornado.ioloop
from tornado.template import Template
from tornado.template import Loader
import sqlite3
import db
import random

class MainHandler(tornado.web.RequestHandler):
    def get(self):
	loader = Loader("./");
	bl = db.getBankList();
	self.write(loader.load("index.html").generate(banks=bl));

class TableHandler(tornado.web.RequestHandler):
    def get(self):
	loader = Loader("./");
	bl = db.getBankList();
        bl = bl[:int(len(bl)*random.random())]
	self.write(loader.load("table.html").generate(banks=bl));

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/assets/css/(.*)", tornado.web.StaticFileHandler, {"path": "./assets/css/"}),
    (r"/assets/js/(.*)", tornado.web.StaticFileHandler, {"path": "./assets/js/"}),
    (r"/assets/img/(.*)", tornado.web.StaticFileHandler, {"path": "./assets/img/"}),
    (r"/table.html", TableHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
    ]);

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
