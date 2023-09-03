
from flask import Flask, render_template, escape, request, redirect
import pandas as pd
import numpy as np
import csv
import math
from sklearn import neighbors, datasets
from numpy.random import permutation
from sklearn.metrics import precision_recall_fscore_support

app = Flask(__name__, static_folder='../static', template_folder='../static')
cs_file = "cetpuc.csv"
data = pd.read_csv(cs_file)
processed_data = data[['kcet', 'puc', 'college']]
random_indices = permutation(data.index)
test_cutoff = math.floor(len(data)/5)
print(test_cutoff)
test = processed_data.loc[random_indices[1:test_cutoff]]
train = processed_data.loc[random_indices[test_cutoff:]]
train_output_data = train['college']
print("train Output data", train_output_data)
train_input_data = train
train_input_data = train_input_data.drop('college',1)
print("train input data", train_input_data)
test_output_data = test['college']
print("test Output data", test_output_data)
test_input_data = test
test_input_data = test_input_data.drop('college',1)
print("test input data", test_input_data)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graduate')
def graduate():
    return render_template('graduate.html')

@app.route("/main")
def return_main():
    return render_template('index.html')



def euclideanDistance(data1, data2, length):
    distance = 0
    for x in range(length):
        distance += np.square(data1[x] - data2[x])
    return np.sqrt(distance)


def knn(trainingSet, testInstance, k):
    print(k)
    distances = {}
    sort = {}
    length = testInstance.shape[1]

    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet.iloc[x], length)

        distances[x] = dist[0]

    sorted_d = sorted(distances.items(), key=lambda x: x[1])

    neighbors = []

    for x in range(k):
        neighbors.append(sorted_d[x][0])

    classVotes = {}

    for x in range(len(neighbors)):
        response = trainingSet.iloc[neighbors[x]][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1

    sortedVotes = sorted(classVotes.items(), key=lambda x: x[1], reverse=True)

    return (sortedVotes, neighbors)




@app.route('/graduatealgo')
def graduatealgo():
    data = pd.read_csv('cetpuc.csv')

    kcet = float(request.args.get("kcet"))
    puc = float(request.args.get("puc"))
    testSet = [[kcet, puc]]
    test = pd.DataFrame(testSet)
    k = 5
    result, neigh = knn(processed_data, test, k)
    list1 = []
    list2 = []
    for i in result:
        list1.append(i[0])
    for i in result:
        list2.append(i[1])
    for i in list1:
        print(i)
    return '''
        <html>
            <head>
                <title>Engineering College Predictor</title>

                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
                <link href="http://getbootstrap.com/examples/jumbotron-narrow/jumbotron-narrow.css" rel="stylesheet">
            </head>
            <body>
                <div class="container">
                    <nav class="navbar navbar-expand-md navbar-dark bg-dark">
                        <h3 class="navbar-brand">College Recommendation</h3>
                        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExample05" aria-controls="navbarsExample05" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarsExample05">
                            <ul class="navbar-nav mr-auto">
                                <li class="nav-item active">
                                    <a class="nav-link" href="/main">Home</a>
                                </li>
                                
                                
                            </ul>
                        </div>
                    </nav>
                </div>

                <div class="container">
                    <div class="jumbotron">
                        <h1>Engineering College Predictor</h1>
                        <p class="lead"></p>
                            <p>
                                The top recommended Colleges based on Karnataka CET rank and PUC percentage are 
                            </p>
                            <table>

                            <tr><td><h4>S.No</h4></td><td><h4>ENGINEERING COLLEGES</h4></td></tr>
                            <tr><td><p>1. </p></td><td>{result10}</td></tr>
                            <tr><td><p>2. </p></td><td>{result20}</td></tr>
                            <tr><td><p>3. </p></td><td>{result30}</td></tr>
                            <tr><td><p>4. </p></td><td>{result40}</td></tr>
                            <tr><td><p>5. </p></td><td>{result50}</td></tr>
                            
                            </table>
                    </div>
                    <button onclick="window.location.href = 'https://www.google.com/maps';">Click Here for location</button>

                    <footer class="footer">
                    </footer>
                </div>
            </body>
        </html>
            '''.format(result10=list1[0], result20=list1[1], result30=list1[2], result40=list1[3], result50=list1[4])


if __name__ == '__main__':
    app.run()
