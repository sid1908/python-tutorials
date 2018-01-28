from flask import Flask, render_template
app = Flask(__name__)


@app.route('/welcome/<name>')
def welcome(name):
    return 'Hello, {}'.format(name.capitalize())

@app.route('/double/<int:num>')
def double(num):
    return '{}'.format(2 * num)


if __name__ == '__main__':
    app.run(debug = True)
