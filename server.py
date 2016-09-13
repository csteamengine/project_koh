#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line
import os
import uuid
import base64
import random
import koh_api


define("port", default=8888, help="run on the given port", type=int)
__INDEX_FILE__ = "client/index.html"
__UPLOADS__ = "/" + "uploads/"
__ASYNC_UPLOAD__ = "async_upload/"
# TODO: Tweak the confidence_threshold to find a good balance for recognition
# A lower confidence value means it's a closer match. So everything less than
# confidence_threshold will constitute a match, and everything above it will
# mean it's not a match.
confidence_threshold = 100
saved_faces_path = "./saved_faces"
koh = koh_api.KohFaceRecognizer(confidence_threshold, saved_faces_path)
# we gonna store clients in dictionary..
clients = dict()
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}


def main():
    # Train all the saved faces into koh
    koh.train_saved_faces()

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


# noinspection PyAbstractClass
class IndexHandler(tornado.web.RequestHandler):
    """
    Handles requests for the '/' url (the index.html page).
    """
    @tornado.web.asynchronous
    def get(self):
        self.render(os.path.dirname(__file__) + "/" + __INDEX_FILE__)


# noinspection PyAbstractClass
class BadRequestHandler(tornado.web.RequestHandler):
    """
    Redirects all bad requests to the index page.
    """
    @tornado.web.asynchronous
    def get(self):
        self.redirect("/")


# noinspection PyAbstractClass
class Upload(tornado.web.RequestHandler):
    # TODO
    """
    What does this do?
    """
    def post(self):
        # noinspection SpellCheckingInspection
        file_info = self.request.files['filearg'][0]
        print("file_info is", file_info)
        f_name = file_info['filename']
        extn = os.path.splitext(f_name)[1]
        c_name = str(uuid.uuid4()) + extn
        if not os.path.isdir(os.path.dirname(__file__) + __UPLOADS__):
            os.mkdir(os.path.dirname(__file__) + __UPLOADS__)

        fh = open(os.path.dirname(__file__) + __UPLOADS__ + c_name, 'wb')
        fh.write(file_info['body'])
        self.redirect("/")      # Sends the url back


# noinspection PyAbstractClass
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    # TODO
    """
    What does this do?
    """

    def open(self, *args):
        # noinspection PyAttributeOutsideInit
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


# noinspection PyAbstractClass
class WebSocketImage(tornado.websocket.WebSocketHandler):
    """
    Handles incoming images that need to be identified by Koh.
    """

    def open(self, *args):
        # noinspection PyAttributeOutsideInit
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}

    def on_message(self, message):
        message = message.split(',')
        f_name = message[2]
        extn = os.path.splitext(f_name)[1]
        c_name = str(uuid.uuid4()) + extn

        if not os.path.isdir(os.path.dirname(__file__) + __UPLOADS__):
            os.mkdir(os.path.dirname(__file__) + __UPLOADS__)

        # Save the uploaded image to the uploads directory
        image_file_path = os.path.dirname(__file__) + __UPLOADS__ + c_name
        print("Saved uploaded image as: {}".format(image_file_path))
        with open(image_file_path, "wb") as fh:
            fh.write(base64.b64decode(message[1]))

        # Use koh to detect and predict a face from the image
        results = koh.predict_face(image_file_path)
        for result in results:
            self._handle_koh_result(result)

        # If it didn't detect a face at all...
        if len(results) == 0:
            send_string = "{},{},{}_{},{},{}".format("", False, "", "", 0, "Unable to detect a face in this image!")
            self.write_message(send_string)

        # Clean things up by deleting the upload file
        os.remove(image_file_path)

    def _handle_koh_result(self, result):
        print("Prediction Result:\n    student_id: {}\n    confidence: {}".format(result.student_id, result.confidence))
        # Is the image a match?
        positive_id = koh.positively_identified(result)
        student_id = result.student_id if positive_id else random.randint(1000000, 9999999)

        # Save the result image
        result_image_path = koh.save_student_image(result.numpy_image, student_id)
        with open(result_image_path, "rb") as image_file:
            encoded_image_string = base64.b64encode(image_file.read())

        # Set send_string properties
        if positive_id:
            first_name, last_name = koh_api.get_name(student_id)
        else:
            first_name, last_name = "", ""

        # In case the student isn't found in the database
        if first_name is None or last_name is None:
            first_name, last_name = "", ""
            positive_id = False

        # send_string format: encoded_image_string, positive_id, first_name, last_name, student_id, error_string
        # If there's an error, return something in the error_string
        send_string = "{},{},{}_{},{},{}".format(
            encoded_image_string, positive_id, first_name, last_name, student_id, "")
        print("""\
Sent back to client:
    image:       {}
    positive_id: {}
    first_last:  {}_{}
    student_id:  {}
    error:       {}""".format(result_image_path, positive_id, first_name, last_name, student_id, ""))

        # Send the string back to the client
        self.write_message(send_string)

    def on_close(self):
        if self.id in clients:
            del clients[self.id]


# noinspection PyAbstractClass
class WebSocketStudent(tornado.websocket.WebSocketHandler):
    # TODO
    """
    What does this do?
    """

    def open(self, *args):
        # self.id = self.get_argument("Id")
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
