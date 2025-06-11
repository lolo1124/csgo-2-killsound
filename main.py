from flask import Flask, request
from playsound import playsound
import threading
import json
import sys
import os

app = Flask(__name__)
previous_kills = 0

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

@app.route('/', methods=['POST'])
def gsi():
    global previous_kills
    data = request.json

    print(json.dumps(data, indent=2))

    if not data or "player" not in data:
        return '', 204

    state = data["player"].get("state", {})
    round_kills = state.get("round_kills", 0)

    if round_kills > previous_kills:
        print("Kill detected!")
        threading.Thread(target=playsound, args=(resource_path("killsound.wav"),)).start()

    previous_kills = round_kills
    return '', 200

if __name__ == '__main__':
    app.run(host='localhost', port=3000)
