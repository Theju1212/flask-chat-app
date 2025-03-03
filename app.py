from flask import Flask, render_template
from flask_socketio import SocketIO, send
from os import getenv

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
    elif isinstance(data, dict):  # Ensure it's a dictionary
        username = data.get("username", "Anonymous").strip()
        message = data.get("message", "").strip()
    else:
        print("Invalid message format received!")
        return

    if message:  # Prevent empty messages
        full_message = f"{username}: {message}"
        print(f"Received: {full_message}")
        chat_history.append(full_message)
        send({"username": username, "message": message}, broadcast=True)  # Send as a dictionary

if __name__ == "__main__":
    print("\U0001F680 Starting Flask SocketIO Chat Server...")
    port = int(getenv("PORT", 10000))  # Default to 10000 if PORT is not set
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
