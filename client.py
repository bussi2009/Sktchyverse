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
        #*****************************************
        self.stroke = []  

        self.canvas.bind('<ButtonPress-1>', self.start_stroke)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.end_stroke)
        #*****************************************
    def draw(self, event):
        x, y = event.x, event.y
        self.canvas.create_line(points, fill='black', width=brush_size, smooth=True)
        
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

#**************************************************************************************************


    def start_stroke(self, event):
        self.stroke = [(event.x, event.y)]

    def draw(self, event):
        self.stroke.append((event.x, event.y))
        if len(self.stroke) >= 3:
            points = [coord for point in self.stroke[-3:] for coord in point]
            self.canvas.create_line(points, fill='black', width=3, smooth=True)

            data = pickle.dumps(('stroke', points))
            self.sock.send(data)

    def end_stroke(self, event):
        self.stroke = []
        

    def receive_data(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                message = pickle.loads(data)
                if message[0] == 'stroke':
                    _, points = message
                    self.canvas.create_line(points, fill='red', width=3, smooth=True)








if __name__ == "__main__":
    root = tk.Tk()
    app = paintclient(root)
    root.mainloop()