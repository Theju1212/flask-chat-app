from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store messages for chat history
chat_history = []

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def handle_message(msg):
    if msg.strip():  # Prevent empty messages
        print(f"Received message: {msg}")
        chat_history.append(msg)
        socketio.send(msg, broadcast=True)  # Broadcast message to all clients

if __name__ == "__main__":
    print("🚀 Starting Flask SocketIO Chat Server...")
    socketio.run(app, host="0.0.0.0", port=10000, debug=True)
