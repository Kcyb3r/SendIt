import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def send_file(file_path, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        with open(file_path, 'rb') as f:
            s.sendall(f.read())
        messagebox.showinfo("Success", f"File {os.path.basename(file_path)} sent successfully!")

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        send_file(file_path, '127.0.0.1', 65432)  # Change host and port as needed

def create_gui():
    root = tk.Tk()
    root.title("File Sender")

    send_button = tk.Button(root, text="Send File", command=select_file)
    send_button.pack(pady=20)

    root.geometry("300x100")
    root.mainloop()

if __name__ == "__main__":
    create_gui()
