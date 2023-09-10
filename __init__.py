from flask import Flask, render_template, flash, request, redirect, url_for
app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/main/', methods=["GET", "POST"])
def mainPage():
    if request.method == "POST":
        entered = request.form

        enteredPointsOfProblem = entered['maxScore']
        enteredNoofPeopleSolvedProblem = entered['noOfSolves']

        if enteredNoofPeopleSolvedProblem.isdigit():
            enteredNoofPeopleSolvedProblem = int(
                enteredNoofPeopleSolvedProblem)
        else:
            enteredNoofPeopleSolvedProblem = -1

        if enteredPointsOfProblem.isdigit():
            enteredPointsOfProblem = int(enteredPointsOfProblem)
        else:
            enteredPointsOfProblem = -1

        if (enteredPointsOfProblem == -1) or (enteredNoofPeopleSolvedProblem == -1):
            return render_template("error.html")

        from sklearn import svm
        import re

        with open('test.txt', 'w') as test:
            testData = str(enteredPointsOfProblem) + '|' + \
                str(enteredNoofPeopleSolvedProblem) + '|' + str(1300) + '|' + str("Easy")
            test.write(testData)

        def resolve(rating):
            difficulty = ""
            if (rating <= 1200):
                difficulty = "Easy"
            elif (rating >= 1200 and rating <= 1700):
                difficulty = "Medium"
            elif (rating >= 1700 and rating <= 2200):
                difficulty = "Hard"
            else:
                difficulty = "Very Hard"
            return difficulty

            # Returns feature & label arrays [ points, solved, rating, difficulty ]
        def parseData(data):
            points = list()
            solved = list()
            rating = list()
            difficulty = list()

            with open(data) as f:
                for line in f:
                    if line != "":
                        all = line.replace('\n', '').split("|")
                        points.append(float(all[0]))
                        solved.append(int(all[1]))
                        rating.append(int(all[2]))
                        difficulty.append(all[3])
            return [points,  solved, rating, difficulty]

        # Prepare the data
        trainingData = parseData('trainingData.txt')
        testingData = parseData('test.txt')

        # A SVM Classifier
        clf = svm.SVC(kernel='linear', C=1.0)
        X = list()
        y = trainingData[2]
        for i in range(len(trainingData[0])):
            X.append([trainingData[0][i],trainingData[1][i]])

        clf = clf.fit(X, y)

        prediction = clf.predict([[testingData[0][0], testingData[1][0]]])
        predicted = resolve(int(prediction[0]))

    return render_template("main.html", predicted=predicted, target=len(trainingData[1]))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
