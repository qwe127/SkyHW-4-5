from app.dao.models.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        return self.session.query(Movie).get(mid)

    def get_all(self):
        return self.session.query(Movie).all()

    def get_by_directors(self, did):
        return self.session.query(Movie).filter(Movie.director_id.like(did))

    def get_by_genre(self, gid: int):
        return self.session.query(Movie).filter(Movie.genre_id.like(gid))

    def get_by_year(self, year: int):
        return self.session.query(Movie).filter(Movie.year.like(year))

    def create(self, data):
        movie = Movie(**data)

        self.session.add(movie)
        self.session.commit()

        return movie

    def update(self, movie):
        self.session.add(movie)
        self.session.commit()

        return movie

    def delete(self, mid):
        movie = self.get_one(mid)

        self.session.delete(movie)
        self.session.commit()

        return movie
