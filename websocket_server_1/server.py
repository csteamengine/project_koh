#!/usr/bin/env python3

import asyncio
import datetime
import random
import signal
import sys
import websockets


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
    # Client list, using the websocket's ID as the Client ID
    clients = []

    def __init__(self):
        self.server = websockets.server.WebSocketServer(None)

    def start(self):
        self.server = websockets.serve(self.handle_connected, self.bind_ip, self.bind_port)
        print("[*] Listening on {}:{}".format(self.bind_ip, self.bind_port))
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    def kill(self):
        print("  Killing the server...", end="")
        try:
            self.server.close()
        except Exception as err:
            print("done with Exception: {}".format(err))
            sys.exit(0)
        print("done.")
        sys.exit(0)

    async def handle_connected(self, websocket, path):
        client_id = id(websocket)
        self.clients.append(client_id)
        print("[*] Client {} has connected.     Num. Clients = {}".format(client_id, len(self.clients)))

        client = KohClient(client_id, websocket, path)

        while websocket.state == websockets.server.OPEN:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            await client.send_message(now)
            await asyncio.sleep(random.random() * 3)


class KohClient:
    def __init__(self, client_id, websocket, path):
        self.client_id = client_id
        self.websocket = websocket
        self.path = path
        self.listen_for_messages()

    def listen_for_messages(self):
        while self.websocket.state == websockets.server.OPEN:
            message = self.websocket.recv()
            print("[*] Message from Client {}:\n{}".format(self.client_id, message))

        # Once the websocket is no longer OPEN, disconnect
        self.disconnect()

    async def send_message(self, message):
        if self.websocket.state == websockets.server.OPEN:
            await self.websocket.send(message)
        else:
            self.disconnect()

    def disconnect(self):
        KohServer.clients.remove(self.client_id)
        print("[*] Client {} has disconnected.  Num. Clients = {}".format(self.client_id, len(KohServer.clients)))


if __name__ == "__main__": main()
