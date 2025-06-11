import tkinter as tk
import pickle
import threading
import socket

HOST = 'localhost'
PORT = 5500

# Making the variable that stors the drawing color
drawing_color = 'red'

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
        
         # UI elements:
        # Button to change color to blue
        top_frame = tk.Frame(self.master)
        top_frame.pack()

        color_button = tk.Button(top_frame,  bg="blue", command=lambda: self.change_color('blue'), width=2, height=2)
        color_button.grid(row=0, column=1, padx=1, pady=1)

        color_button = tk.Button(top_frame,  bg="red", command=lambda: self.change_color('red'), width=2, height=2)
        color_button.grid(row=0, column=2, padx=1, pady=1)

        color_button = tk.Button(top_frame,  bg="green", command=lambda: self.change_color('green'), width=2, height=2)
        color_button.grid(row=0, column=3, padx=1, pady=1)

        color_button = tk.Button(top_frame,  bg="yellow", command=lambda: self.change_color('yellow'), width=2, height=2)
        color_button.grid(row=2, column=1, padx=1, pady=1)

        color_button = tk.Button(top_frame,  bg="grey", command=lambda: self.change_color('grey'), width=2, height=2)
        color_button.grid(row=2, column=2, padx=1, pady=1)

        color_button = tk.Button(top_frame,  bg="black", command=lambda: self.change_color('black'), width=2, height=2)
        color_button.grid(row=2, column=3, padx=1, pady=1)

    def change_color(self, color):
        global drawing_color
        drawing_color = color


        self.stroke = []  

    def draw(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x, y, x+4, y+4, fill=drawing_color, outline=drawing_color)
        data = pickle.dumps((x, y))
        self.sock.send(data)

    def receive_data(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                x, y = pickle.loads(data)
                self.canvas.create_oval(x, y, x+4, y+4, fill=drawing_color, outline=drawing_color)
            except:
                break




    def start_stroke(self, event):
        self.stroke = [(event.x, event.y)]

    def draw(self, event):
        self.stroke.append((event.x, event.y))
        if len(self.stroke) >= 3:
            points = [coord for point in self.stroke[-3:] for coord in point]
            self.canvas.create_line(points, fill=drawing_color, width=3, smooth=True)

            data = pickle.dumps(('stroke', points))
            self.sock.send(data)

    def end_stroke(self, event):
        self.stroke = []
        

    # def receive_data(self):
    #     while True:
    #         try:
    #             data = self.sock.recv(4096)
    #             if not data:
    #                 break
    #             message = pickle.loads(data)
    #             if message[0] == 'stroke':
    #                 _, points = message
    #                 self.canvas.create_line(points, fill='red', width=3, smooth=True)








if __name__ == "__main__":
    root = tk.Tk()
    app = paintclient(root)
    root.mainloop()