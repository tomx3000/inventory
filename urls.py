from django.conf.urls import url
from django.urls import  path,include

from . import views


urlpatterns = [
path('home/nine', views.MyView.as_view(),name='fbv'),
]