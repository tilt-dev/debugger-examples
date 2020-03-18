from random import choice

from flask import Flask, render_template
app = Flask(__name__)

CHOICES = ["✨", "🎉", "🤖", "🐢", "👍", "🐙", "👋", "👀"]


@app.route("/")
def serve():
    # from remote_pdb import RemotePdb; RemotePdb('127.0.0.1', 5555).set_trace()
    return choice(CHOICES)


if __name__ == "__main__":
    CHOICES = ["😬"]
    app.run(port=8000, debug=True)
