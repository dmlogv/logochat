__title__ = 'Logochat Client GUI'
__version__ = '0.0.1'


import logging
import socket
import threading
import time
import tkinter as tk
from tkinter import ttk as ttk
from tkinter import scrolledtext

import client


logging.info(f'{__title__} {__version__} Started')


class Gui(ttk.Frame):
    def __init__(self, host='127.0.0.1', port=30000, buffer_size=1024):
        tk.Frame.__init__(self, None)
        self.pack(padx=3, pady=3, fill=tk.BOTH, expand=True)
        self.winfo_toplevel().title(__title__)

        # Widgets
        self.messages = None
        self.input = None
        self.create_widgets()

        # Client opening
        self.client = client.Client(
            host=host,
            port=port,
            buffer_size=buffer_size,
            target=self.insert_message
            )

    def __del__(self):
        self.client = None

    def create_widgets(self):
        self.messages = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.messages.config(state=tk.DISABLED)
        self.messages.pack(fill=tk.BOTH)

        self.input = tk.Entry(self)
        self.input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input.focus_set()
        self.input.bind('<Return>', self.send_handler)

    def send_handler(self, e):
        text = e.widget.get()
        self.client.send(text)
        e.widget.delete(0, tk.END)

    def insert_message(self, text):
        self.messages.config(state=tk.NORMAL)
        self.messages.insert(tk.INSERT, text + '\n')
        self.messages.config(state=tk.DISABLED)

            
