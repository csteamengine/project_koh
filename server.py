#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line
import os, uuid
import base64
import koh_api


define("port", default=8888, help="run on the given port", type=int)
__INDEX_FILE__ = "client/index.html"
__UPLOADS__ = "/" + "uploads/"
__ASYNC_UPLOAD__ = "async_upload/"
koh = koh_api.KohFaceRecognizer()
# we gonna store clients in dictionary..
clients = dict()
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
id = 0


def main():
    # This  part is the key to success. We have to redirect the websocket calls to a different URL ex//: /websocket
    app = tornado.web.Application([
        (r'/', IndexHandler),
        (r'/websocket', WebSocketHandler),
        (r'/uploads', Upload),
        (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
        (r'/websocket_image', WebSocketImage),
        (r'/websocket_newstudent', WebSocketStudent),
        (r'.*', BadRequestHandler)
    ], **settings)
    parse_command_line()
    app.listen(options.port)
    print("Listening on port {}".format(options.port))
    tornado.ioloop.IOLoop.instance().start()


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render(os.path.dirname(__file__) + "/" + __INDEX_FILE__)


class BadRequestHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.redirect("/")


class Upload(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        print("fileinfo is", fileinfo)
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        if not os.path.isdir(os.path.dirname(__file__) + __UPLOADS__):
            os.mkdir(os.path.dirname(__file__) + __UPLOADS__)

        fh = open(os.path.dirname(__file__) + __UPLOADS__ + cname, 'wb')
        fh.write(fileinfo['body'])
        self.redirect("/")      # Sends the url back


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}
        self.write_message("WebSocket was successfully connected to server!")

    def on_message(self, message):
        """
        when we receive some message we want some message handler..
        for this example i will just print message to console
        """
        print("Message received from Client %s : %s" % (self.id, message))

    def on_close(self):
        if self.id in clients:
            del clients[self.id]

    def send_message_to_client(self, message):
        """
        The given message prints to the browser console.
        :param message: The text you want to send.
        """
        self.write_message(message)


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

        if not os.path.isdir(os.path.dirname(__file__) + __UPLOADS__):
            os.mkdir(os.path.dirname(__file__) + __UPLOADS__)

        # Save the uploaded image to the uploads directory
        image_file_path = os.path.dirname(__file__) + __UPLOADS__ + cname
        with open(image_file_path, "wb") as fh:
            fh.write(base64.b64decode(message[1]))

        # Use koh to detect and predict a face from the image
        results = koh.predict_face(image_file_path)
        # TODO

        with open(os.path.dirname(__file__) + "/" + "saved_faces/student811699925.000.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        """TODO Use opencv to determine if recognized (ie. returns id)
            With id call database to get first and last get_name(id)"""
        recognized = False
        first = "Charlie"
        last = "Steenhagen"

        """send_string = "{},Charlie_Steenhagen".format(encoded_string)"""
        send_string = "{},{},{}_{},{}".format(encoded_string, recognized, first, last, id)

        # first_name = ""
        # last_name = ""
        # identified = True
        # student_name = "{}_{}".format(first_name, last_name)
        # student_id = ""
        #
        # # FORMAT: Image, True/False, Name, ID
        # send_string = "{},{},{},{}".format(encoded_string, identified, student_name, student_id)

        self.write_message(send_string)

    def on_close(self):
        if self.id in clients:
            del clients[self.id]


class WebSocketStudent(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        """self.id = self.get_argument("Id")"""
        print("open student ws")

    def on_message(self, message):
        message = message.split(',')
        # id = message[0]
        first = message[0]
        last = message[1]
        print("First name: " + first)
        print("Last name: " + last)
        self.write_message("SUCCESS")
        # TODO uncomment when ready write_new(id, first, last)

    def on_close(self):
        print("Closed")


if __name__ == '__main__':
    main()