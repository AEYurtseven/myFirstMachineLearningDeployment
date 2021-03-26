#This is Heroku Deployment Lectre
from flask import Flask, request, render_template
import os
import pickle

print("Test")
print(os.getcwd())
path = os.getcwd()

with open('Models/Pickle_RL_Model.pkl', 'rb') as f:
    logistic = pickle.load(f)

##with open('Models/RF_model.pkl', 'rb') as f:
##    randomforest = pickle.load(f)

##with open('Models/svm_clf_model.pkl', 'rb') as f:
##    svm_model = pickle.load(f)


def get_predictions(price, Tax, Driver_Age, Licence_Length_Years, req_model):
    mylist = [Driver_Age, Tax, price, Licence_Length_Years]
    mylist = [float(i) for i in mylist]
    vals = [mylist]

    if req_model == 'Logistic':
        #print(req_model)
        return logistic.predict(vals)[0]

##    elif req_model == 'RandomForest':
##        #print(req_model)
##        return randomforest.predict(vals)[0]

#    elif req_model == 'SVM':
#        #print(req_model)
#        return svm_model.predict(vals)[0]
    else:
        return "Cannot Predict"


app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def my_form_post():
    if request.method == 'POST':
        price = request.form['age']
        Tax = request.form['sex']
        Driver_Age = request.form['cp']
        Licence_Length_Years = request.form['trestbps']
        req_model = request.form['req_model']

        target = get_predictions(price, Tax, Driver_Age, Licence_Length_Years, req_model)

        if target==1:
            sale_making = 'Customer is likely to have a heart disease'
        else:
            sale_making = 'Customer is unlikely to have a heart disease'

        return render_template('home.html', target = target, sale_making = sale_making)
    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)