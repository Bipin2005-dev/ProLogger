from flask import Flask
from flask_cors import CORS
from flask import request
import subprocess

app = Flask("ProLogger")
CORS(app)

@app.route('/', methods=['POST'])
def fileReceiver():
    if request.method == "POST":
        og_file = request.files['raw-log']
        og_file.save(f"./uploadedFile.log")
        subprocess.run(["bash log_to_csv.sh ./uploadedFile.log ./processed_upload.log"], shell=True)
        subprocess.run(["python ./plotter.py ./processed_upload.log ./output_plots"], shell=True)
        return "<p>Yaaay!!</p>"
