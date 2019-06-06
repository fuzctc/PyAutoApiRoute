import tornado.ioloop
import tornado.web

from routers import NestedRouter, GenericRouter
from handlers.main import MainHandler
# r = GenericRouter("/api/", trailing_slash=False)
r = NestedRouter("/api/", trailing_slash=False)
# r.register(r"/clusters/(?P<cluster_id>[^/.]+)/pods", MainHandler)
r.register(("clusters", "pods"), MainHandler)
# r.register(r"/me", MainHandler)
r.register(r"me", MainHandler)
for i in r.rules:
    print(i)


def make_app():
    return tornado.web.Application(r.rules)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
