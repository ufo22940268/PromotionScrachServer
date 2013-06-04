import tornado.web
import tornado.ioloop
from tornado.template import Template
from tornado.template import Loader
import sqlite3
import db

class MainHandler(tornado.web.RequestHandler):
    def get(self):
	loader = Loader("./");
	bl = db.getBankList();
	self.write(loader.load("index.html").generate(banks=bl));

class ContentHandler(tornado.web.RequestHandler):

    class Entity:
        pass

    def get(self):
        loader = Loader("./");
        self.write(loader.load("content.html").generate(**(self.build_values())));

    def build_values(self):
        conn = get_connection();
        c = conn.cursor();
        c.execute("SELECT title, url FROM blog");
        rows = c.fetchall();
        entities = [];
        for row in rows:
            entity = ContentHandler.Entity();
            entity.content = row[0];
            entity.url = row[1];
            entities.append(entity);
        return {"entities" : entities};

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/assets/css/(.*)", tornado.web.StaticFileHandler, {"path": "./assets/css/"}),
    (r"/assets/js/(.*)", tornado.web.StaticFileHandler, {"path": "./assets/js/"}),
    (r"/assets/img/(.*)", tornado.web.StaticFileHandler, {"path": "./assets/img/"}),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
    ]);

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
