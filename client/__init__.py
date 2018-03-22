__title__ = 'Logochat Client'
__version__ = '0.0.1'


import logging
import socket
import threading
import time
import tkinter as tk
from tkinter import ttk as ttk
from tkinter import scrolledtext


logging.info(f'{__title__} {__version__} Started')


class Client:
    QUIT = '/quit'
    CONNECT = '/connect'
    
    def __init__(self, host='127.0.0.1', port=12345, buffer_size=1024, target=print):
        logging.debug(f'{self.__class__.__name__} created')
        self.host = host
        self.port = port
        self.buffer_size = buffer_size

        logging.debug(f'We will use target: {target}')
        self.target = target

        self.socket = None
        self.receive_thread = None
        
        # self.connect()
        
    def __del__(self):
        self.disconnect()

    def connect(self, retry=5, delay=10):
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
            except OSError as e:
                if retry:
                    logging.error(f'Connection error: {e}\nI will try {retry} times with {delay} delay')
                    retry -= 1
                    time.sleep(delay)
                else:
                    raise
            else:   
                self.receive_thread = threading.Thread(target=self.receive)
                self.receive_thread.start()
                logging.debug(self.socket) 
                break

    def disconnect(self):
        self.receive_thread = None

    def receive(self):
        while True:
            try:
                if self.receive_thread:
                    msg = self.socket.recv(self.buffer_size).decode('utf8')
                    self.target(msg)
                else:
                    raise SystemError('Thread closed')
            except OSError as e:
                self.connect()
                break
                
    def send(self, msg):
            if msg == Client.QUIT:
                self.socket.send(bytes(Client.QUIT, 'utf8'))
                self.disconnect()
            if msg == Client.CONNECT:
                self.connect()
            else:
                self.socket.send(bytes(msg, 'utf8'))

            
