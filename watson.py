from __future__ import print_function
import json
import requests
import time
import urllib
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, EmotionOptions
import psycopg2
conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")

TOKEN = "802624766:AAGFeusIY0pHAjasyJiheR14QD6mjDsIclE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def natural_languaje(message):
    # If service instance provides API key authentication
    service = NaturalLanguageUnderstandingV1(
        version='2018-03-16',
        ## url is optional, and defaults to the URL below. Use the correct URL for your region.
        url='https://gateway-wdc.watsonplatform.net/natural-language-understanding/api',
        iam_apikey='SsR_VL-lpJpVRWAVc3mQKek9G35-GVLxKhTlUfA9AsRf')

    # service = NaturalLanguageUnderstandingV1(
    #    version='2018-03-16',
    #    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    #    url='https://gateway-wdc.watsonplatform.net/natural-language-understanding/api',
    #    username='auto-generated-apikey-69bba0f9-fecf-46c8-828b-925ea2f7f000',
    #    password='SsR_VL-lpJpVRWAVc3mQKek9G35-GVLxKhTlUfA9AsRf')

    response = service.analyze(
        text=message,
        features=Features(entities=EntitiesOptions(),
                          keywords=KeywordsOptions(),
                          emotion=EmotionOptions())).get_result()

    return response

def calculate_emotions(message):
    emotions = {"sadness": 0, "joy": 0, "fear": 0, "disgust": 0, "anger": 0}
    data = natural_languaje((message["result"])[0]["message"]["text"])
    emotions["sadness"] += data["emotion"]["document"]["emotion"]["sadness"]
    emotions["joy"] += data["emotion"]["document"]["emotion"]["joy"]
    emotions["fear"] += data["emotion"]["document"]["emotion"]["fear"]
    emotions["disgust"] += data["emotion"]["document"]["emotion"]["disgust"]
    emotions["anger"] += data["emotion"]["document"]["emotion"]["anger"]
    return emotions

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def postgres_test():
    try:
        conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114",
                                port="54321")
        conn.close()
        return True
    except:
        return False

def echo_all(updates, conn):
    cur = conn.cursor()
    for update in updates["result"]:
        print(update)

        #send_message(text, chat)

        message_id = update['message']['message_id']
        user_id = update['message']['from']['id']
        user_name = str(update['message']['from']['first_name'])
        user_last = str(update['message']['from']['last_name'])
        chat_id = update['message']['chat']['id']
        chat_title = str(update['message']['chat']['title'])
        chat_type = str(update['message']['chat']['type'])
        message_date = update['message']['date']
        message_text = str(update['message']['text'])
        print(message_text)
        print(message_id)

        try:
            print(calculate_emotions(updates))
            processed_message = calculate_emotions(updates)
            sadness = processed_message['sadness']
            joy = processed_message['joy']
            fear = processed_message['fear']
            disgust = processed_message['disgust']
            anger = processed_message['anger']

            cur.execute("insert into message(message_id, user_id, user_name, user_last, chat_id, "
                        "chat_title, chat_type, message_date, text, sadness, joy, "
                        "fear, disgust, anger) values({}, {} ,'{}' ,'{}' ,{},'{}' ,'{}',{},'{}',{},{},{},{},{})".format(
                message_id, user_id, user_name, user_last, chat_id, chat_title,
                chat_type, message_date, message_text, sadness, joy, fear, disgust, anger
            ))

            conn.commit()


        except Exception as e:
            print('is except')
            cur.execute("insert into message(message_id, user_id, user_name, user_last, chat_id, "
                        "chat_title, chat_type, message_date, text, sadness, joy, "
                        "fear, disgust, anger) values({}, {} ,'{}' ,'{}' ,{},'{}' ,'{}',{},'{}',{},{},{},{},{})".format(
                message_id, user_id, user_name, user_last, chat_id, chat_title,
                chat_type, message_date, message_text, 0.0, 0.0, 0.0, 0.0, 0.0
            ))

            conn.commit()
            print(e)


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    print(updates)

    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


last_update_id = None
while True:
    updates = get_updates(last_update_id)
    try:
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates, conn)
            #print(type(views.calculate_emotions(updates)))
        time.sleep(0.5)
        #natural_languaje((updates["result"])[0]["message"]["text"])
    except:
        break
