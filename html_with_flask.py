from flask import Flask, render_template, redirect, url_for,request


app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/fail/<int:score>')
def fail(score):
    return "Person has failed.Marks are " + str(score)

@app.route('/passed/<int:score>')
def passed(score):
    return "Person has passed.Marks are " + str(score)


@app.route('/results/<int:marks>')
def results(marks):
    result = ''
    if marks < 50:
       result = 'fail'
    else:
       result = 'pass'
    return redirect(url_for(result,score=marks))

@app.route('/submit',methods = ['GET','POST'])
def submit():
    total_score = 0
    if request.method == 'POST':
        science = float(request.form['science'])
        maths = float(request.form['maths'])
        computer = float(request.form['computer'])
        hindi = float(request.form['hindi'])
        total_score = (science + maths + computer + hindi)/4
        
    res = ''
    if total_score >= 50:
        res = 'passed' #we want to redirect to passed page
    else:
        res = 'fail' ##we want to redirect to fail page
    return redirect(url_for(res,score=total_score))


if __name__ =='__main__':
   app.run(debug=True)