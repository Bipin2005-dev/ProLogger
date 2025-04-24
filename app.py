from flask import Flask, render_template, jsonify, redirect, url_for, send_from_directory
from flask import request
import subprocess
import time
import numpy as np
import os

app = Flask("ProLogger")
file_uploaded = False #Global variable to check if it is the first time for the user uploading a file, in which case the table and graphs from the nav bar shouldn't be available.

@app.route('/', methods=['GET'])
def index():
           return redirect(url_for('home'))
@app.route('/index', methods=['GET'])
def home():
    return render_template('index.html', file_uploaded=file_uploaded)

@app.route('/fileProcess', methods=['POST'])
def fileUpload():
    file = request.files['raw-log']
    if file:
        if os.path.exists('./temp/output_plots/bar_plot.png'):
            os.remove('./temp/output_plots/bar_plot.png')
        if os.path.exists('./temp/output_plots/pie_plot.png'):
            os.remove('./temp/output_plots/pie_plot.png')
        if os.path.exists('./temp/output_plots/line_plot.png'):
            os.remove('./temp/output_plots/line_plot.png')
        file.save('./temp/uploadedFile.log')
        subprocess.run(["bash ./scripts/log_to_csv.sh ./temp/uploadedFile.log ./temp/processedUpload.log"], shell=True)
        try:
            with open("./temp/processedUpload.log", "r") as file:
                error_check = file.readline()
                if error_check.startswith("Invalid format"):
                    return render_template('processing.html', event="Invalid file")
                elif error_check.startswith("Empty file"):
                    return render_template('processing.html', event="Empty file")
        except UnicodeDecodeError:
            return "<p>Unicode Error</p>"
        subprocess.run(["python3 ./scripts/plotter.py ./temp/processedUpload.log ./temp/output_plots/"], shell=True)
    else:
        return render_template('processing.html', event="File not found")
    file_uploaded = True
    return redirect(url_for('table'))

@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
    if request.method == "GET":
        return render_template('graphs.html', file_uploaded=True)
    elif request.method == "POST":
        start_time = request.form['start_time'] if request.form['start_time'] != '' else '00:00:00'
        end_time = request.form['end_time'] if request.form['end_time'] != '' else '00:00:00'
        start_datetime = f"{request.form['start_date']}T{start_time}+05:30"
        end_datetime = f"{request.form['end_date']}T{end_time}+05:30"
        subprocess.run([f"bash ./scripts/filter.sh ./temp/processedUpload.log {start_datetime} {end_datetime} ./temp/filtered.log"],shell=True)
        subprocess.run(["python3 ./scripts/plotter.py ./temp/filtered.log ./temp/output_plots/"], shell=True)
        return render_template('graphs.html', file_uploaded=True)

@app.route('/temp/<path:filename>', methods=['GET'])
def temp(filename: str):
    return send_from_directory('temp', filename)


@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'GET':
        tokenized_lines = np.loadtxt('temp/processedUpload.log', delimiter=',', skiprows=1, dtype=object)
        return render_template('table.html', tokens = tokenized_lines, file_uploaded=True)

    if request.method == 'POST':
        start_time = request.form['start_time'] if request.form['start_time'] != '' else '00:00:00'
        end_time = request.form['end_time'] if request.form['end_time'] != '' else '00:00:00'
        start_datetime = f"{request.form['start_date']}T{start_time}+05:30"
        end_datetime = f"{request.form['end_date']}T{end_time}+05:30"
        subprocess.run([f"bash ./scripts/filter.sh ./temp/processedUpload.log {start_datetime} {end_datetime} ./temp/filtered.log"],shell=True)
        tokenized_lines = np.loadtxt('temp/filtered.log', delimiter=',', dtype=object)
        return render_template('table.html', tokens = tokenized_lines, file_uploaded=True)

if __name__ == '__main__':
    app.run(debug=True)
