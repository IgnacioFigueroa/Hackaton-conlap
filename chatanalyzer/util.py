from django.http import JsonResponse
import psycopg2
from . import views
conn = psycopg2.connect(database="grupo3", user="grupo3", password="2gKdbj", host="201.238.213.114", port="54321")

def get_chart_info(request):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM message")
    rows = cursor.fetchall()
    data = []
    for id, message_id, user_id, user_name, user_last, chat_id, chat_title, chat_type, message_date, text, sadness, joy, fear, disgust, anger in rows:
        data.append({"joy":joy, "sadness":sadness, "fear":fear, "disgust":disgust, "anger": anger, "text": text, "date":message_date})

    return JsonResponse(views.emotions_graph_data(data), safe=False)

def get_messages_info(request):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM message")
    rows = cursor.fetchall()
    data = []

    for id, message_id, user_id, user_name, user_last, chat_id, chat_title, chat_type, message_date, text, sadness, joy, fear, disgust, anger in rows:
        sum = sadness+joy+fear+disgust+anger
        if sum<1.2:
            sum = 'I'
        else:
            sum = 'R'
        data.append({"id":id, "message_id": message_id, "user_id":user_id, "user_name": user_name, "user_last": user_last,
                     "message_date":message_date,"text": text, "emotions_sum":sum})

    return JsonResponse(data, safe=False)
