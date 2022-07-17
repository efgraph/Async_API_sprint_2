from django.urls import path, include
from .views import FilmworkList, FilmworkDetail


urlpatterns = [
    path('v1/movies/', FilmworkList.as_view()),
    path('v1/movies/<uuid:pk>', FilmworkDetail.as_view())
]
