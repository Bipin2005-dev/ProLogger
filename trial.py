from flask import Flask
from flask import render_template
from flask_cors import CORS
from flask import request

app = Flask("ProLogger")
CORS(app)

@app.route('/', methods=['POST'])
def fileReceiver():
    if request.method == "POST":
        og_file = request.files['raw-log']
        og_file.save(f"./uploadedFile.log")
        return "<p>Yaaay!!</p>"
