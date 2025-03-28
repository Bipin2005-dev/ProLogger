from flask import Flask

app = Flask("ProLogger")

@app.route('/')
def hello():
    return '<p>Hello World!</p>'