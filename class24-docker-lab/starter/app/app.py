from flask import Flask, jsonify
import os, socket

app = Flask(__name__)

@app.get("/")
def hello():
    who = os.getenv("WHO", "Docker Learner")
    return f"""
    <html>
      <head><title>Hello, Compose!</title></head>
      <body style="font-family: system-ui; padding: 2rem">
        <h1>Hello, {who} 👋</h1>
        <p>Served from: <code>{socket.gethostname()}</code></p>
        <p>Try <a href="/health">/health</a>.</p>
      </body>
    </html>
    """

@app.get("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
