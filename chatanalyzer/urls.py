from django.urls import path
from . import views, util

urlpatterns = [
    path('', views.index, name='index'),
    path('get_chart_data/', util.get_chart_info, name="chart_data"),
    path('get_messages/', util.get_messages_info, name="get_messages")
]
