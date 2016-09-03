#!/usr/bin/env python3
import signal
import sys
import socket
import threading
from time import sleep


def main():
    koh_server = KohServer()

    # Setup the SIGINT catcher to kill the server when Ctrl+C is pressed
    def signal_handler(signal, frame):
        koh_server.kill()
    signal.signal(signal.SIGINT, signal_handler)

    koh_server.start()


class KohServer:
    # Server config information
    bind_ip = "localhost"  # Use this for development
    # bind_ip = socket.gethostname()       # Use this if this gets moved to an actual server
    bind_port = 8000

    def start(self):
        # Start the server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._bind_server()

        while True:
            client, addr = self.server.accept()

            print("[*] Accepted connection from {}:{}".format(addr[0], addr[1]))

            # spin up our client thread to handle incoming data
            client_handler = threading.Thread(target=KohServer.handle_client, args=(client, addr))
            client_handler.start()

    # Binds the server to the address and port
    def _bind_server(self, timeout=60):
        bound_successfully = False
        attempts = 0
        print("[*] Attempting to connect to {}:{}".format(self.bind_ip, self.bind_port), end='')
        while not bound_successfully and attempts < timeout:
            try:
                self.server.bind((self.bind_ip, self.bind_port))
                print()
                bound_successfully = True
            except:
                print('.', end='', flush=True)
                attempts += 1
                sleep(1)

        if not bound_successfully:
            print("Timed out after {} seconds. Exiting program.".format(timeout))
            sys.exit(1)

        self.server.listen(5)
        print("[*] Listening on {}:{}".format(self.bind_ip, self.bind_port))

    # Handles client threads
    @staticmethod
    def handle_client(client_socket, addr):
        # print out what the client sends
        request = client_socket.recv(1024)
        decoded_string = bytes(request).decode("unicode_escape")   # Escaped characters like newline are decoded
        print("[*] Received: \n{}".format(decoded_string))

        if r"GET / HTTP/1.1" in decoded_string:
            print("[*] Returning index.html")
            index_file = open("http/index.html", "r", encoding="utf-8")
            index_file_content = ''.join(index_file.readlines())
            response = '''\
HTTP/1.1 200 OK
Date: Thu, 20 May 2004 21:12:58 GMT
Connection: close
Server: ProjectKohServer
Accept-Ranges: bytes
Content-Type: text/html
Content-Length: {}
Last-Modified: Tue, 18 May 2004 10:14:49 GMT

{}'''.format(len(index_file_content), index_file_content)
            print("[*] Sent: \n{}".format(response))
            client_socket.send(bytes(response.encode()))
        else:
            client_socket.send(bytes("ACK!".encode()))

        # send back a packet
        # packet = r"HTTP/1.1 200 OK\nContent-Type: text/html\n\n<body><h1>Hello World!</h1></body>"
        # client_socket.send(bytes(packet.encode()))

        client_socket.close()
        print("[*] Closed connection to {}:{}".format(addr[0],addr[1]))

    def kill(self):
        print("  Killing the server...", end="")
        try:
            self.server.shutdown(socket.SHUT_RDWR)
            self.server.close()
        except:
            print("done. (Transport endpoint was not connected)")
            sys.exit(0)
        print("done.")
        sys.exit(0)


# Starts the main process
if __name__ == "__main__": main()
