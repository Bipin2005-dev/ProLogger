from flask import Flask, render_template, jsonify, redirect, url_for, send_from_directory
from flask import request
import subprocess
import time
import numpy as np

app = Flask("ProLogger")

@app.route('/index', methods=['GET'])
def home():
    return render_template('index.html')

#TODO: Implement error checks for the uploaded file and prevent the website from crashing.
@app.route('/fileProcess', methods=['POST'])
def fileUpload():
    file = request.files['raw-log']
    if file:
        file.save('./temp/uploadedFile.log')
        subprocess.run(["bash ./scripts/log_to_csv.sh ./temp/uploadedFile.log ./temp/processedUpload.log"], shell=True)
        try:
            with open("./temp/processedUpload.log", "r") as file:
                error_check = file.readline()
                print(error_check)
                if error_check.startswith("Invalid format"):
                    return render_template('processing.html', event="Invalid file") 
        except UnicodeDecodeError:
            return "<p>Unicode Error</p>"
        subprocess.run(["python3 ./scripts/plotter.py ./temp/processedUpload.log ./temp/output_plots/"], shell=True)
    else:
        return render_template('processing.html', event="File not found") 
    return redirect(url_for('table'))

@app.route('/analytics', methods=['GET'])
def analytics():
    return render_template('analytics.html')

@app.route('/temp/<path:filename>', methods=['GET'])
def temp(filename: str):
    return send_from_directory('temp', filename)

#Parsing Sun Dec 04 04:44:54 2005 to 2005-12-04T04:44:54
def datetime_converter(og_date : str):
    _, month, date, _time, year = og_date.split(" ")
    month_dict = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
    }
    output = f"{year}-{month_dict[month]}-{date}T{_time}"
    return output

@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'GET':
        tokenized_lines = np.loadtxt('temp/processedUpload.log', delimiter=',', skiprows=1, dtype=object)
        return render_template('table.html', tokens = tokenized_lines)

    if request.method == 'POST':
        tokenized_lines = np.loadtxt('temp/processedUpload.log', delimiter=',', skiprows=1, dtype=object)
        start_datetime = f"{request.form['start-date']}T{request.form['start-time']}"
        end_datetime = f"{request.form['end-date']}T{request.form['end-time']}"
        mask = [True if (end_datetime >= datetime_converter(datetime) >= start_datetime) else False for datetime in tokenized_lines.T[1]]
        tokenized_lines = tokenized_lines[mask]
        return render_template('table.html', tokens = tokenized_lines)

if __name__ == '__main__':
    app.run(debug=True)
