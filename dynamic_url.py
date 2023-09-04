from flask  import Flask,redirect,url_for
import pandas

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Hello World!'


@app.route('/success/<int:score>')
def success(score):
    return "Person has passed and marks are " + str(score)

@app.route('/fail/<int:score>')
def fail(score):
    return "Person has failed and marks are " + str(score)

@app.route('/results/<int:marks>')
def results(marks):
    result = ''
    if marks<50:
        result = "fail"
    else:
        result = "success"
    return redirect(url_for(result,score=marks))    

if __name__ =='__main__':
    app.run(debug=True)