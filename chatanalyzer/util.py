from __future__ import print_function
import json
import requests
import time
import urllib
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, EmotionOptions

TOKEN = "802624766:AAGFeusIY0pHAjasyJiheR14QD6mjDsIclE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def echo_all(updates):
    for update in updates["result"]:

        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            return {"chat_id": chat,"text":text}
        except Exception as e:
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


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            return echo_all(updates)
        time.sleep(0.5)


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

    print(json.dumps(response, indent=2))

