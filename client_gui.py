import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, message + "\n")
            chat_box.config(state=tk.DISABLED)
            chat_box.yview(tk.END)
        except:
            messagebox.showerror("Error", "Disconnected from server!")
            client.close()
            break

# Function to send a message
def send_message():
    message = message_entry.get()
    if message:
        client.send(message.encode())
        message_entry.delete(0, tk.END)

# Function to close the chat window
def on_closing():
    client.send("quit".encode())  # Inform server before closing
    client.close()
    window.destroy()

# Create the client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 7007))

# Create GUI window
window = tk.Tk()
window.title("Chat App")
window.geometry("400x500")

# Chat display area
chat_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20)
chat_box.pack(pady=10)

# Message input field
message_entry = tk.Entry(window, width=40)
message_entry.pack(pady=5)

# Send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# Start receiving messages in a thread
threading.Thread(target=receive_messages, daemon=True).start()

# Handle window closing
window.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI
window.mainloop()
