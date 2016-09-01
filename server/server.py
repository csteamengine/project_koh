import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print(self.data)
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())
        self.request.send('Hello from the other side!!!!')

if __name__ == "__main__":
    HOST, PORT = "localhost", 8000

    # Create the server, binding to localhost on port 8000
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()