import tkinter as tk
import pickle
import threading
import socket

HOST = 'localhost'
PORT = 5500

class paintclient:
    def __init__(self, master):
        self.master = master
        self.master.title("sketchyverse: Demo")
        self.canvas = tk.Canvas(master, width=800, height=600, bg='white')
        self.canvas.pack()

        self.canvas.bind('<B1-Motion>', self.draw)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        threading.Thread(target=self.receive_data, daemon=True).start()

    def draw(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x, y, x+4, y+4, fill='blue', outline='blue')
        data = pickle.dumps((x, y))
        self.sock.send(data)

    def receive_data(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                x, y = pickle.loads(data)
                self.canvas.create_oval(x, y, x+4, y+4, fill='red', outline='red')
            except:
                break






if __name__ == "__main__":
    root = tk.Tk()
    app = paintclient(root)
    root.mainloop()