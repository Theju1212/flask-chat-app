from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store messages for chat history
chat_history = []

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def handle_message(data):
    if isinstance(data, str):  # Support both string and dictionary format
        message = data.strip()
        username = "Anonymous"
    else:
        username = data.get("username", "Anonymous")
        message = data.get("message", "").strip()

    if message:  # Prevent empty messages
        full_message = f"{username}: {message}"
        print(f"Received: {full_message}")
        chat_history.append(full_message)
        send(full_message, broadcast=True)  # Broadcast to all clients

if __name__ == "__main__":
    print("🚀 Starting Flask SocketIO Chat Server...")
    socketio.run(app, host="0.0.0.0", port=10000, debug=True)
