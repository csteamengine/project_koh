import socket
import threading

bind_ip   = "localhost"
bind_port = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

print("[*] Listening on {}:{}".format(bind_ip, bind_port))

# this is our client-handling thread

def handle_client(client_socket):
    # print out what the client sends
    request = client_socket.recv(1024)

    print("[*] Received: {}".format(request))

    # # send back a packet
    # str = "ACK!"
    client_socket.send(bytes())

    client_socket.close()

while True:
    client,addr = server.accept()

    print("[*] Accepted connection from {}:{}".format(addr[0],addr[1]))

    # spin up our client thread to handle incoming data
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()