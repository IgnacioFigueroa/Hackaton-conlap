from django.http import JsonResponse
import psycopg2
from . import views
from statistics import mean
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
    # ----
    predominant_emotions_in_conversation = []
    sums = []
    mayores = []
    proms = []
    c = 0
    f = 0
    relevant = "I"

    for r in rows:
        more_mayor = False
        quiebre = False
        mayor_al_promedio = False
        print(r)
        emotions = ["sadness", "joy", "fear", "disgust", "anger"]
        mayor = max([r[10], r[11], r[12], r[13], r[14]])
        print("suma de emociones:", sum([r[10], r[11], r[12], r[13], r[14]]))
        sums.append(sum([r[10], r[11], r[12], r[13], r[14]]))
        this_emotion = emotions[r.index(mayor) - 10]
        if (mayor == 0 or mayor == 0.0) and len(predominant_emotions_in_conversation) > 0:
            this_emotion = predominant_emotions_in_conversation[-1]
        mayores.append(mayor)
        proms.append(mean(sums))
        print("promedio:", proms[-1])
        if sum([r[10], r[11], r[12], r[13], r[14]]) > proms[-1] - 1:
            mayor_al_promedio = True
            if sum([r[10], r[11], r[12], r[13], r[14]]) > proms[-1] + 1:
                more_mayor = True
        print(mayor, this_emotion)
        if len(predominant_emotions_in_conversation) > 0:
            if this_emotion != predominant_emotions_in_conversation[-1]:
                quiebre = True
                print("QUIEBRE")
        predominant_emotions_in_conversation.append(this_emotion)
        if mayor_al_promedio:
            print("---  MENSAJE RELEVANTE  ----")
            relevant = "R"
            if more_mayor and quiebre:
                relevant = "RI"
            c += 1
        f += 1
        data.append({"id": r[0], "message_id": r[1], "user_id": r[2], "user_name": r[3], "user_last": r[4],
                     "message_date": r[8], "text": r[9], "emotions_sum": relevant})
    print("contador:", c, "de", f)
    # ---
    return JsonResponse(data, safe=False)
