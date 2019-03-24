from django.http import JsonResponse
import psycopg2
from . import views
from statistics import mean
from datetime import datetime
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
    cursor.execute("SELECT * FROM message ORDER BY id")
    rows = cursor.fetchall()
    data = []
    # ----
    predominant_emotions_in_conversation = []
    sums = []
    proms = []
    c, f, mr = 0, 0, 0

    for r in rows:
        relevant = "I"
        quiebre = False
        mayor_al_promedio = False
        #print(r)
        emotions = ["sadness", "joy", "fear", "disgust", "anger"]
        number_emotions = [r[10], r[11], r[12], r[13], r[14]]
        mayor = max(number_emotions)
        #print("suma de emociones:", sum(number_emotions))

        if sum(number_emotions) != 0:
            sums.append(sum(number_emotions))
            this_emotion = emotions[r.index(mayor) - 10]
            if (mayor == 0 or mayor == 0.0) and len(predominant_emotions_in_conversation) > 0:
                this_emotion = predominant_emotions_in_conversation[-1]
            proms.append(mean(sums))
            #print("promedio:", proms[-1])
            if sum(number_emotions) > proms[-1]:
                mayor_al_promedio = True
            #print(mayor, this_emotion)
            if len(predominant_emotions_in_conversation) > 0:
                if this_emotion != predominant_emotions_in_conversation[-1]:
                    quiebre = True
                    #print("QUIEBRE")
            predominant_emotions_in_conversation.append(this_emotion)
            if mayor_al_promedio:
                #print("---  MENSAJE RELEVANTE  ----")
                relevant = "R"
                if quiebre:
                    relevant = "RI"
                    #print("---  MENSAJE  M U Y   RELEVANTE  ----")
                    mr += 1
            c += 1
        f += 1
        date = datetime.fromtimestamp(r[8]).strftime("%A, %B %d, %Y %I:%M:%S")
        'Sunday, January 29, 2017 08:30:00'
        data.append({"id": r[0], "message_id": r[1], "user_id": r[2], "user_name": r[3], "user_last": r[4],
                     "message_date": date, "text": r[9], "emotions_sum": relevant})
    # ---
    return JsonResponse(data, safe=False)
