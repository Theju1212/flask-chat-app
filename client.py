import socket
import threading
import os
import time

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(message)  # Print received messages
        except:
            print("\n❌ Disconnected from server.")
            break

# Function to display chat history
def display_chat_history():
    if os.path.exists("chat_history.txt"):
        print("\n📜 Previous Chat History:")
        with open("chat_history.txt", "r", encoding="utf-8") as file:
            for line in file:
                print(line.strip())
        print("📜 End of Chat History\n")

# Function to start the chat client
def start_client():
    while True:  # Auto-reconnect loop
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('your-server-ip', 7007))

            name = input("Enter your name: ")
            client.send(name.encode())

            print("\n✅ Connected to the chat server. Type 'quit' to exit.")
            print("📩 For private messages, use: @username <message>")
            print("👥 Type '@who' to see online users\n")

            # Show previous chat history
            display_chat_history()

            # Start a thread to receive messages
            threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

            while True:
                message = input()
                if message.lower() == "quit":
                    print("🚪 Disconnecting...")
                    client.close()
                    return
                client.send(message.encode())

        except (ConnectionRefusedError, socket.error):
            print("❌ Server not available. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    start_client()
