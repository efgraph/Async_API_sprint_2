import datetime

from rest_framework import serializers

from .models import Filmwork, Genre, GenreFilmwork, PersonFilmwork


class FilmworkSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Filmwork
        fields = ('__all__')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        g = instance.genres.all().values_list('name', flat=True)
        actors = []
        directors = []
        writers = []
        persons = PersonFilmwork.objects.prefetch_related('person').filter(film_work__id=instance.id).values_list(
            'role', 'person__full_name')
        for person in persons:
            if person[0] == 'actor':
                actors.append(person[1])
            if person[0] == 'director':
                directors.append(person[1])
            if person[0] == 'writer':
                writers.append(person[1])
        representation['genres'] = list(g)
        representation['actors'] = list(actors)
        representation['directors'] = list(directors)
        representation['writers'] = list(writers)
        representation['creation_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
        representation.pop('persons')
        representation.pop('created')
        representation.pop('modified')
        return representation

    def get_rating(self, obj):
        if obj.rating:
            return obj.rating
        return 0


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('__all__')


class GenreFilmworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreFilmwork
        fields = ('__all__')
