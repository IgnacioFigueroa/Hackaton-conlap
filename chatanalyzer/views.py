from django.shortcuts import render
from django.http import HttpResponse
from . import util
import re
import operator
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, EmotionOptions


def index(request):

    return render(request, 'home.html', {})


def emotions_graph_data(messages):
    emotions = {'sadness': 0.0, 'joy': 0.0, 'fear': 0.0, 'disgust': 0.0, 'anger': 0.0}
    prevalent = []
    amount = 0
    #time = []
    lower = len(messages)
    timestamps = [[]]
    graph_data = [["x", "Score"]]
    count = 0
    for i in range(len(messages)):
        if (lower/10)*(count+1) > i:
            timestamps[count].append(messages[i])
        else:
            timestamps.append([messages[i]])
            count += 1

    for j in range(len(timestamps)):
        for i in timestamps[j]:
            try:
                sentiments = {'sadness': i["sadness"], 'joy': i["joy"], 'fear': i["fear"], 'disgust': i["disgust"], 'anger': i["anger"]}
                emotions["sadness"] += float(sentiments["sadness"])
                emotions["joy"] += float(sentiments["joy"])
                emotions["fear"] += float(sentiments["fear"])
                emotions["disgust"] += float(sentiments["disgust"])
                emotions["anger"] += float(sentiments["anger"])
            except:
                sentiments = {'sadness': 0, 'joy': 0, 'fear': 0, 'disgust': 0, 'anger': 0}
                continue

        #graph_data[j].append(emotions["sadness"])
        #graph_data[j].append(emotions["joy"])
        #graph_data[j].append(emotions["fear"])
        #graph_data[j].append(emotions["disgust"])
        #graph_data[j].append(emotions["anger"])
        maximum = max(emotions.items(), key=operator.itemgetter(1))[0]
        prevalent.append(maximum)
        amount = (emotions[maximum])
        graph_data.append([j, amount])
        emotions = {'sadness': 0.0, 'joy': 0.0, 'fear': 0.0, 'disgust': 0.0, 'anger': 0.0}

    return graph_data, prevalent


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
