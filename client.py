import tkinter as tk
import pickle
import threading
import socket

HOST = 'localhost'
PORT = 8888

class paintclient:
    def __init__ (self, master):
        self.master = master
        self.master.title("Sketshyverse: Demo")
        self.canvas = tk.canvas(master, width = 900, height = 600, bg = 'white' )
        

