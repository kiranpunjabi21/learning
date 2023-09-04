from flask import Flask


app = Flask(__name__)


@app.route('/')
def welcome():
    return "Hello World!"


@app.route('/2ndpage')
def page():
    return "Second page"


if __name__=="__main__":
    app.run(debug=True)