from django.shortcuts import render
from django.http import HttpResponse
from . import util
import re
import operator
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, EmotionOptions
import psycopg2
from . import views
conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")


def index(request):

    return render(request, 'home.html', {})


def emotions_graph_data(messages):
    emotions = {'sadness': 0.0, 'joy': 0.0, 'fear': 0.0, 'disgust': 0.0, 'anger': 0.0}
    #prevalent = []
    #amount = []
    #time = []
    lower = messages[0]["date"]
    timestamps = [[messages[0]]]
    graph_data = [['Percentage', 'Sadness', 'Joy', 'Fear', 'Disgust', 'Anger'], [str(messages[0]["date"])]]
    count = 0
    for i in messages:
        if lower + 600 > i["date"]:
            timestamps[count].append(i)
        else:
            timestamps.append([i])
            graph_data.append([i["date"]])
            lower = i["date"]
            count += 1

    for j in range(len(timestamps)):
        for i in timestamps[j]:
            try:
                sentiments = [i["sadness"], i["joy"], i["fear"], i["disgust"], i["anger"]]
                emotions["sadness"] += sentiments[0]
                emotions["joy"] += sentiments[1]
                emotions["fear"] += sentiments[2]
                emotions["disgust"] += sentiments[3]
                emotions["anger"] += sentiments[4]
            except:
                continue

        graph_data[j+1].append(emotions["sadness"])
        graph_data[j+1].append(emotions["joy"])
        graph_data[j+1].append(emotions["fear"])
        graph_data[j+1].append(emotions["disgust"])
        graph_data[j+1].append(emotions["anger"])
        #maximum = max(emotions.items(), key=operator.itemgetter(1))[0]
        #prevalent.append(maximum)
        #amount.append(emotions[maximum])

    return graph_data


def calculate_emotions(message):
    emotions = {"sadness": 0.0, "joy": 0.0, "fear": 0.0, "disgust": 0.0, "anger": 0.0}
    try:
        data = util.natural_languaje((message["result"])[0]["message"]["text"])
    except:
        if re.findall("hax*", (message["result"])[0]["message"]["text"]):
            emotions = {"sadness": 0.0, "joy": 0.9, "fear": 0.0, "disgust": 0.0, "anger": 0.0}
        return emotions
    emotions["sadness"] += data["emotion"]["document"]["emotion"]["sadness"]
    emotions["joy"] += data["emotion"]["document"]["emotion"]["joy"]
    emotions["fear"] += data["emotion"]["document"]["emotion"]["fear"]
    emotions["disgust"] += data["emotion"]["document"]["emotion"]["disgust"]
    emotions["anger"] += data["emotion"]["document"]["emotion"]["anger"]
    return emotions
