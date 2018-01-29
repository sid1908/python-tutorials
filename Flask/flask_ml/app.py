import os, sys, shutil, time

from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)


model_directory = 'model'
model_file_name = '%s/model.pkl' % model_directory
model_columns_file_name = '%s/model_columns.pkl' % model_directory

# These will be populated at training time
model_columns = None
clf = None


@app.route('/training')
def training():
    # inputs
    training_data = pd.read_csv('data/titanic.csv')

    training_data.drop(["PassengerId", "Name", "Ticket", "Cabin"], axis = 1, inplace = True)
    training_data.fillna(training_data.mean(), inplace = True)
    training_data.dropna(inplace = True)

    sex = pd.get_dummies(training_data.Sex, drop_first = True)
    embarked = pd.get_dummies(training_data.Embarked, drop_first = True)

    training_data.drop(['Sex', 'Embarked'], axis = 1, inplace = True)

    training_data = pd.concat([sex, embarked, training_data], axis = 1)

    x = training_data.iloc[:, 1:]
    y = training_data.iloc[:, 0]

    # capture a list of columns that will be used for prediction
    global model_columns
    model_columns = list(x.columns)
    joblib.dump(model_columns, model_columns_file_name)

    global clf
    clf = RandomForestClassifier()
    start = time.time()
    clf.fit(x, y)
    print('Trained in %.1f seconds' % (time.time() - start))
    print('Model training score: %s' % clf.score(x, y))

    joblib.dump(clf, model_file_name)

    return 'Success'


@app.route('/predict')
def predict():
    clf = joblib.load(model_file_name)
    print('model loaded')

    prediction = clf.predict([[1, 38.0, 1, 0, 71.2833, 0, 0, 0]])

    return render_template('pos.html', prediction = prediction)

if __name__ == '__main__':
    app.run(debug = True)
