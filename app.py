from flask import Flask, render_template, jsonify, redirect, url_for, send_from_directory
from flask import request
import subprocess
import time

app = Flask("ProLogger")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/fileProcess', methods=['POST'])
def fileUpload():
    render_template('processing.html', event="loading")
    file = request.files['raw-log']
    if file:
        file.save('./temp/uploadedFile.log')
        subprocess.run(["bash ./scripts/log_to_csv.sh ./temp/uploadedFile.log ./temp/processedUpload.log"], shell=True)
        subprocess.run(["python3 ./scripts/plotter.py ./temp/processedUpload.log ./temp/output_plots/"],shell=True)
    else:
        return render_template('processing.html', event="error") 
    return redirect(url_for('analytics'))

@app.route('/analytics', methods=['GET'])
def analytics():
    return render_template('analytics.html')

@app.route('/temp/<path:filename>', methods=['GET'])
def temp(filename: str):
    return send_from_directory('temp', filename)


if __name__ == '__main__':
    app.run(debug=True)
