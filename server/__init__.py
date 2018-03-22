__title__ = 'Logochat Server'
__version__ = '0.0.1'


import logging
import random
import socket
import string
import threading


logging.info(f'{__title__} {__version__} Started')


class Client:
    def generate_name(length=8):
        return ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(length)
            )
    
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.name = Client.generate_name()

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f'<Client {self.name} client="{self.client}" address="{self.address}">'

    def __str__(self):
        return f'<{self.name}>'
    

class Server:
    QUIT = '/quit'
    NAME = '/name'
    
    def __init__(self, host='0.0.0.0', port=30000, buffer_size=1024, max_clients=100):
        logging.debug(f'{self.__class__.__name__} created')
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.max_clients = max_clients

        self.clients = {}
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(self.max_clients)

        self.accept_thread = threading.Thread(target=self.accept_connection)
        self.accept_thread.start()
        self.accept_thread.join()

    def __del__(self):
        self.server.close()
        
    def accept_connection(self):
        while True:
            client = Client(*self.server.accept())
            logging.info(f'{client} connected')

            self.clients[client] = client
            client.socket.send(bytes(f'Hello, {client}', 'utf8'))

            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while True:
            try:
                msg = client.socket.recv(self.buffer_size).decode('utf8')
                logging.info(f'{client} says: {msg}')
            except OSError as e:
                self.disconnect_client(client)
                break
                
            if msg == Server.QUIT:
                self.disconnect_client(client)
                break
            elif msg.startswith(Server.NAME):
                new_name = msg.strip(Server.NAME).strip()
                self.broadcast(f'{client} renames to <{new_name}>')
                client.name = new_name
            else:
                self.broadcast(f'{client} says: {msg}')

    def disconnect_client(self, client):
        logging.info(f'{client} leaves chat')
        try:
            del self.clients[client]
        except KeyError as e:
            logging.error(f'{client} already deleted')
        self.broadcast(f'{client} leaves chat')        

    def broadcast(self, msg):
        for client in self.clients:
            try:
                client.socket.send(bytes(msg, 'utf8'))
            except OSError as e:
                logging.error(e)


