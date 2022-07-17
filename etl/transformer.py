class TransformerUtil:

    @staticmethod
    def transform_film_work(row):
        return {
            'id': row['id'],
            'title': row['title'],
            'description': row['description'],
            'imdb_rating': row['rating'],
            'genre': row['genres'],
            'writers_names': row['writers'],
            'actors_names': row['actors'],
            'actors': [a for a in row['actors_json'] if a],
            'writers': [w for w in row['writers_json'] if w],
            'director': row['directors'],
        }

    @staticmethod
    def transform_genre(row):
        return {
            'id': row['id'],
            'genre': row['name'],
        }

    @staticmethod
    def transform_person(row):
        return {
            'id': row['id'],
            'full_name': row['full_name'],
            'writer': [w for w in "".join(filter(lambda x : x not in ["{", "}"], row['writer'])).split(",") if w],
            'actor': [w for w in "".join(filter(lambda x : x not in ["{", "}"], row['actor'])).split(",") if w],
            'director': [w for w in "".join(filter(lambda x : x not in ["{", "}"], row['director'])).split(",") if w]
        }
