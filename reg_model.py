from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy


app = Flask(__name__)
regmodel = pickle.load(open('reg_model.pkl','rb'))
scaler = pickle.load(open('scaling.pkl','rb'))


@app.route('/')
def index():
    return render_template('reg_model.html')

@app.route('/submit',methods = ['GET','POST'])
def submit():
    output = ''
    if request.method == 'POST':
        crim = float(request.form['crim'])
        znab = float(request.form['znab'])
        indus = float(request.form['indus'])
        chas = float(request.form['chas'])
        nox = float(request.form['nox'])
        rmab = float(request.form['rmab'])
        age = float(request.form['age'])
        dis = float(request.form['dis'])
        rad = float(request.form['rad'])
        tax = float(request.form['tax'])
        ptratio = float(request.form['ptratio'])
        babc = float(request.form['babc'])
        lstat = float(request.form['lstat'])
        lst = [crim, znab, indus, chas, nox, rmab, age, dis,rad, tax, ptratio, babc, lstat]
        new_data = scaler.transform(numpy.array(lst).reshape(1,-1))
        output = regmodel.predict(new_data)[0]
        print(output)
    res = 'res'
    return redirect(url_for(res,medv= output))

@app.route('/res/<float:medv>')
def res(medv):
    return "Median value of owner-occupied homes in $1000's (MEDV)" + str(medv)


if __name__ =='__main__':
    app.run(debug=True)