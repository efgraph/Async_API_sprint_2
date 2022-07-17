from rest_framework import generics
from .models import Filmwork
from .serializers import FilmworkSerializer


class FilmworkList(generics.ListAPIView):
    queryset = Filmwork.objects.all()
    serializer_class = FilmworkSerializer


class FilmworkDetail(generics.RetrieveAPIView):
    queryset = Filmwork.objects.all()
    serializer_class = FilmworkSerializer
