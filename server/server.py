import tornado.ioloop
import tornado.web
import tornado.websocket
import os, uuid
import base64

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
__UPLOADS__ = "uploads/"
__ASYNC_UPLOAD__ = "async_upload/";
# we gonna store clients in dictionary..
clients = dict()


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("../client/html/index.html")


class Upload(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        print("fileinfo is", fileinfo)
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open(__UPLOADS__ + cname, 'wb')
        fh.write(fileinfo['body'])
        self.redirect("/")      # Sends the url back
        # self.render("../client/index.html")
        # self.finish(cname + " is uploaded!! Check %s folder" %__UPLOADS__)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}

    def on_message(self, message):
        """
        when we receive some message we want some message handler..
        for this example i will just print message to console
        """
        print("Client %s received a message : %s" % (self.id, message))
        self.write_message("Hello Client!")

    def on_close(self):
        if self.id in clients:
            del clients[self.id]


class WebSocketImage(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}

    def on_message(self, message):
        message = message.split(',')
        fname= message[2]
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        with open(__UPLOADS__ + cname, "wb") as fh:
            fh.write(base64.b64decode(message[1]))


    def on_close(self):
        if self.id in clients:
            del clients[self.id]


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
# This part is the key to success. We have to redirect the websocket calls to a different URL ex//: /websocket
app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/websocket', WebSocketHandler),
    (r'/uploads', Upload),
    (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    (r'/websocket_image', WebSocketImage)
], **settings)

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()