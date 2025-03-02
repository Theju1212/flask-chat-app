import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from colorama import init, Fore

init(autoreset=True)  # Enable colored text reset automatically

# Standard socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the socket server
def connect_to_server():
    try:
        client.connect(('127.0.0.1', 7007))
        print(Fore.GREEN + "✅ Connected to socket server!")
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"Could not connect to socket server: {e}")

# Receive messages from the server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            display_message(message)
        except:
            messagebox.showerror("Error", "Disconnected from server!")
            client.close()
            break

# Display received messages in chat box
def display_message(data):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, data + "\n", "server")
    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

# Send message to the server
def send_message():
    message = message_entry.get().strip()
    if message:
        data = f"{username.get()}: {message}"  
        client.send(data.encode())  # Send to socket server
        message_entry.delete(0, tk.END)  

# Handle window closing
def on_closing():
    try:
        client.send("quit".encode())  
    except:
        pass
    client.close()
    window.destroy()

# Create GUI window
window = tk.Tk()
window.title("Real-Time Chat")
window.geometry("400x500")

# Username input
username_label = tk.Label(window, text="Username:")
username_label.pack()
username = tk.Entry(window)
username.pack()

# Chat display area
chat_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20)
chat_box.pack(pady=10)

# Message input field
message_entry = tk.Entry(window, width=40)
message_entry.pack(pady=5)

# Send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# Connect to the socket server
connect_to_server()

# Handle window closing
window.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI
window.mainloop()
