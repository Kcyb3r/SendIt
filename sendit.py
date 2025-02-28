import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

# Define color scheme
BACKGROUND_COLOR = "#1E1E1E"
FOREGROUND_COLOR = "#FFFFFF"
BUTTON_COLOR = "#007ACC"
BUTTON_HOVER_COLOR = "#005A9E"

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            with open('received_file', 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
            print("File received successfully!")

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
    root.title("SendIt - File Transfer Tool")
    root.configure(bg=BACKGROUND_COLOR)

    # Set the window to fullscreen with decorations
    root.attributes('-fullscreen', True)
    root.overrideredirect(False)  # Allow window decorations

    # Create a frame for the title bar
    title_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
    title_frame.grid(row=0, column=0, sticky='ew')  # Use grid for the title frame

    # Add a spacer to push buttons to the right
    spacer = tk.Label(title_frame, bg=BACKGROUND_COLOR)
    spacer.grid(row=0, column=0, sticky='ew')  # Add a spacer to fill the space

    # Minimize button
    minimize_button = tk.Button(title_frame, text="_", command=root.iconify, bg=BUTTON_COLOR, fg=FOREGROUND_COLOR)
    minimize_button.grid(row=0, column=1, padx=5)  # Position minimize button

    # Close button
    close_button = tk.Button(title_frame, text="X", command=root.quit, bg=BUTTON_COLOR, fg=FOREGROUND_COLOR)
    close_button.grid(row=0, column=2, padx=5)  # Position close button

    # Title and Action Labels
    banner_label = tk.Label(root, text="Welcome to SendIt!", font=("Helvetica", 16), bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    banner_label.grid(row=1, column=0, pady=(20, 10), padx=20)  # Centered with padding

    action_label = tk.Label(root, text="Choose an action:", font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    action_label.grid(row=2, column=0, pady=(0, 20), padx=20)  # Centered with padding

    # Center the buttons in a new row
    button_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
    button_frame.grid(row=3, column=0, pady=(0, 20), padx=20)  # Centered with padding

    send_button = tk.Button(button_frame, text="Send File", command=select_file, bg=BUTTON_COLOR, fg=FOREGROUND_COLOR)
    send_button.grid(row=0, column=0, padx=10)  # Centered in button frame
    send_button.bind("<Enter>", lambda e: send_button.config(bg=BUTTON_HOVER_COLOR))
    send_button.bind("<Leave>", lambda e: send_button.config(bg=BUTTON_COLOR))

    receive_button = tk.Button(button_frame, text="Start Receiving", command=start_receiving, bg=BUTTON_COLOR, fg=FOREGROUND_COLOR)
    receive_button.grid(row=0, column=1, padx=10)  # Centered in button frame
    receive_button.bind("<Enter>", lambda e: receive_button.config(bg=BUTTON_HOVER_COLOR))
    receive_button.bind("<Leave>", lambda e: receive_button.config(bg=BUTTON_COLOR))

    # Configure grid weights for better resizing
    root.grid_rowconfigure(0, weight=0)  # Title bar
    root.grid_rowconfigure(1, weight=0)  # Banner label
    root.grid_rowconfigure(2, weight=0)  # Action label
    root.grid_rowconfigure(3, weight=1)  # Button frame

    # Center the button frame vertically
    button_frame.grid_rowconfigure(0, weight=1)  # Center buttons in button frame

    root.mainloop()

def start_receiving():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    messagebox.showinfo("Info", "Server started. Waiting for incoming files...")

if __name__ == "__main__":
    create_gui() 