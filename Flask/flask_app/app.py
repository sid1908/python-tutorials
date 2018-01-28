from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask'

@app.route('/hello')
def hello():
    return 'Hello world'


if __name__ == '__main__':
    app.run(debug = True)
