#!/usr/bin/env python3

from pathlib import Path
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
# enable CORS for all routes
CORS(app)

allowed_projects = {"tsip"}


@app.route('/')
def api_hello_world():
    return 'Root endpoint'


@app.route('/read')
def api_read():
    return "Not allowed"


@app.route('/log', methods=['GET', 'POST'])
def api_log():
    if request.content_type != 'application/json':
        return "Invalid content type " + request.content_type

    data = request.get_json()
    if data["project"] not in allowed_projects:
        return "Invalid project"


    # make sure the directory exits
    path_file = "data/" + data["project"] + "/" + data["uid"] + ".jsonl"
    path_dir = "/".join(path_file.split("/")[:-1])
    if ".." in path_file or "~" in path_file:
        return "Invalid path"
        
    Path(path_dir).mkdir(parents=True, exist_ok=True)

    with open(path_file, "a") as f:
        f.write(data["payload"] + "\n")

    return "OK"

# pythonanywhere does not want us to launch the app by ourselves
# so make sure we don't do that when it's being important and won't
# block the port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# app.run()
