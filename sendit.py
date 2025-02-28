import socket
import os
import tkinter as tk
from tkinter import filedialog, simpledialog
import threading
from datetime import datetime
import platform
import uuid
import ssl

# Define color scheme
BACKGROUND_COLOR = "#1E1E1E"
FOREGROUND_COLOR = "#FFFFFF"
BUTTON_COLOR = "#007ACC"
BUTTON_HOVER_COLOR = "#005A9E"

# Directory to save received files
RECEIVED_FILES_DIR = "received_files"

# Password for authentication
AUTH_PASSWORD = "securepassword"  # Change this to a secure password

# Global variable for the selected file path
file_path = None

def start_server(host='127.0.0.1', port=65432):
    if not os.path.exists(RECEIVED_FILES_DIR):
        os.makedirs(RECEIVED_FILES_DIR)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print(f"Server listening on {host}:{port}")
            conn, addr = s.accept()
            with conn:
                try:
                    # Use default SSL context
                    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                    conn = context.wrap_socket(conn, server_side=True)
                    print(f"Connected by {addr}")

                    password = conn.recv(1024).decode()
                    if password != AUTH_PASSWORD:
                        print("Authentication failed.")
                        return

                    filename = conn.recv(1024).decode()
                    filename = os.path.basename(filename)
                    received_file_path = os.path.join(RECEIVED_FILES_DIR, filename)

                    if os.path.exists(received_file_path):
                        print(f"File '{filename}' already exists. Aborting transfer.")
                        return

                    with open(received_file_path, 'wb') as f:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            f.write(data)
                    show_message(f"File '{filename}' received successfully!")
                    add_to_history(addr[0], filename)

                except Exception as e:
                    print(f"Error during connection handling: {e}")

    except Exception as e:
        print(f"Error starting server: {e}")

def send_file(file_path, host, port):
    context = ssl.create_default_context()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            s = context.wrap_socket(s, server_hostname=host)

            s.sendall(AUTH_PASSWORD.encode())
            s.sendall(os.path.basename(file_path).encode())
            with open(file_path, 'rb') as f:
                s.sendall(f.read())
            show_message(f"File '{os.path.basename(file_path)}' sent successfully!")
        except Exception as e:
            print(f"Error sending file: {e}")

def select_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        root.after(1000, lambda: send_file(file_path, '127.0.0.1', 65432))
        file_name_label.config(text=os.path.basename(file_path))
        loading_effect()

def toggle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes('-fullscreen', is_fullscreen)

def loading_effect():
    file_name_label.config(text="Loading...")
    root.after(2000, lambda: file_name_label.config(text=""))

def show_message(message):
    message_label.config(text=message)

def add_to_history(machine_name, file_name):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_entry = f"{current_time} - {machine_name} - {file_name}"
    history_listbox.insert(tk.END, history_entry)

def create_gui():
    global root, is_fullscreen, file_name_label, message_label, history_listbox, connected_label
    is_fullscreen = False

    root = tk.Tk()
    root.title("SendIt - File Transfer Tool")
    root.configure(bg=BACKGROUND_COLOR)
    root.geometry("800x600")
    root.eval('tk::PlaceWindow . center')

    title_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
    title_frame.grid(row=0, column=0, sticky='ew')

    spacer = tk.Label(title_frame, bg=BACKGROUND_COLOR)
    spacer.grid(row=0, column=0, sticky='ew')

    minimize_button = tk.Button(title_frame, text="_", command=root.iconify, bg=BUTTON_COLOR, fg=FOREGROUND_COLOR)
    minimize_button.grid(row=0, column=1, padx=5)

    close_button = tk.Button(title_frame, text="X", command=root.quit, bg=BUTTON_COLOR, fg=FOREGROUND_COLOR)
    close_button.grid(row=0, column=2, padx=5)

    fullscreen_button = tk.Button(title_frame, text="#", command=toggle_fullscreen, bg=BUTTON_COLOR, fg=FOREGROUND_COLOR)
    fullscreen_button.grid(row=0, column=3, padx=5)

    banner_label = tk.Label(root, text="Welcome to SendIt!", font=("Helvetica", 16), bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    banner_label.grid(row=1, column=0, pady=(20, 10), padx=20, sticky='nsew')

    action_label = tk.Label(root, text="Choose an action:", font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    action_label.grid(row=2, column=0, pady=(0, 20), padx=20, sticky='nsew')

    button_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
    button_frame.grid(row=3, column=0, pady=(0, 20), padx=20)

    send_button = tk.Button(button_frame, text="Send File", command=select_file, bg=BUTTON_COLOR, fg=FOREGROUND_COLOR)
    send_button.grid(row=0, column=0, padx=10)
    send_button.bind("<Enter>", lambda e: send_button.config(bg=BUTTON_HOVER_COLOR))
    send_button.bind("<Leave>", lambda e: send_button.config(bg=BUTTON_COLOR))

    receive_button = tk.Button(button_frame, text="Start Receiving", command=start_receiving, bg=BUTTON_COLOR, fg=FOREGROUND_COLOR)
    receive_button.grid(row=0, column=1, padx=10)
    receive_button.bind("<Enter>", lambda e: receive_button.config(bg=BUTTON_HOVER_COLOR))
    receive_button.bind("<Leave>", lambda e: receive_button.config(bg=BUTTON_COLOR))

    right_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
    right_frame.grid(row=0, column=1, sticky='ns')

    connected_label = tk.Label(right_frame, text="Connected Machine: 127.0.0.1", font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    connected_label.pack(pady=(20, 10))

    file_name_label = tk.Label(right_frame, text="", font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    file_name_label.pack(pady=(0, 20))

    message_label = tk.Label(root, text="", font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    message_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))

    history_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
    history_frame.grid(row=7, column=0, columnspan=2, pady=(10, 0), padx=20)

    history_label = tk.Label(history_frame, text="Received Files History:", font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    history_label.pack(pady=(0, 5))

    history_listbox = tk.Listbox(history_frame, width=50, height=10, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    history_listbox.pack(pady=(0, 10))

    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=1)

    button_frame.grid_rowconfigure(0, weight=1)

    root.mainloop()

def start_receiving():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    show_message("Server started. Waiting for incoming files...")  # Show message in the center

if __name__ == "__main__":
    create_gui() 