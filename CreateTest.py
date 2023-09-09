import csv
import requests as r
import json

url = "https://codeforces.com/api/problemset.problems"
data = r.get(url).text
json_data = json.loads(data)

problem = json_data["result"]["problems"]
problemStats = json_data["result"]["problemStatistics"]


def resolve(arr):
    new_arr = list()
    for i in range(len(arr)):
        rating = arr[i]
        if (rating <= 1200):
            new_arr.append("Easy")
        elif (rating >= 1200 and rating <= 1700):
            new_arr.append("Medium")
        elif (rating >= 1700 and rating <= 2200):
            new_arr.append("Hard")
        else:
            new_arr.append("Very Hard")
    return new_arr


x1 = list()
x2 = list()
y = list()

itr = 0
NO_OF_TRAINING_DATA_SET = 100
while (len(x1) != NO_OF_TRAINING_DATA_SET):
    t1 = problem[itr]
    t2 = problemStats[itr]
    if ("points" in t1) and ("rating" in t1) and ("solvedCount" in t2):
        x1.append(problem[itr]["points"])
        y.append(problem[itr]["rating"])
        x2.append(problemStats[itr]["solvedCount"])
    itr += 1

d = y
d = resolve(d)

with open('trainingData.txt', 'w') as txtfile:
    for i in range(NO_OF_TRAINING_DATA_SET):
        txtfile.write(str(x1[i]) + '|' + str(x2[i]) +
                      '|' + str(y[i]) + '|' + str(d[i]) + '\n')
print("File created Succesfully")
