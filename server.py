import socket
import threading
import os
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)

clients = {}  # Dictionary to store connected clients

# Function to log messages
def save_message(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")  
    formatted_message = f"{timestamp} {message.strip()}"
    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(formatted_message + "\n")

# Function to broadcast messages
def broadcast(message, sender_name="Server"):
    for name, client in list(clients.items()):
        if name != sender_name:  
            try:
                client.send(message.encode())
            except:
                client.close()
                del clients[name]  

# Function to send private messages
def send_private_message(message, sender_name, client_socket):
    parts = message.split(" ", 1)
    if len(parts) < 2:
        client_socket.send("⚠ Invalid format! Use @username <message>\n".encode())
        return

    target_name = parts[0][1:].strip()
    private_message = parts[1]

    target_client = clients.get(target_name)
    if target_client:
        private_msg = f"[Private] {sender_name} -> {target_name}: {private_message}"
        target_client.send(private_msg.encode())
        save_message(private_msg)
    else:
        client_socket.send(f"❌ User '{target_name}' not found.\n".encode())

# Function to handle each client
def handle_client(client_socket):
    global clients
    try:
        name = client_socket.recv(1024).decode('utf-8').strip()

        # Ignore health checks or malformed names
        if name.startswith("HEAD") or name.startswith("GET"):
            print(f"⚠️ Ignoring non-chat request: {name}")
            client_socket.close()
            return

        clients[name] = client_socket
        print(Fore.GREEN + f"✅ {name} has joined the chat.")
        broadcast(f"📢 {name} has joined the chat!")

        # Send chat history
        if os.path.exists("chat_history.txt"):
            with open("chat_history.txt", "r", encoding="utf-8") as file:
                client_socket.send("\n📜 Previous Chat History:\n".encode())
                for line in file:
                    client_socket.send(line.encode())
                client_socket.send("\n📜 End of Chat History\n".encode())

        # Listen for messages
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            print(Fore.YELLOW + f"📩 {name}: {message}")
            save_message(f"{name}: {message}")

            if message.startswith("@who"):
                online_users = "👥 Online Users: " + ", ".join(clients.keys())
                client_socket.send(online_users.encode())
            elif message.startswith("@"):  # Private message
                send_private_message(message, name, client_socket)
            else:
                broadcast(f"{name}: {message}", name)
    except Exception as e:
        print(f"❌ Error handling client {name}: {e}")

    finally:
        # Ensure safe deletion
        if name in clients:
            del clients[name]
        print(Fore.RED + f"❌ {name} has left the chat.")
        broadcast(f"📢 {name} has left the chat!")
        client_socket.close()

# Function to start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 7007))
    server.listen()

    print(Fore.CYAN + "🚀 Server is listening on 127.0.0.1:7007...")

    while True:
        client_socket, address = server.accept()
        print(Fore.BLUE + f"🔌 Connection from {address} established!")

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
