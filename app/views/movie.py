from flask import request
from flask_restx import Resource, Namespace

from app.dao.models.movie import MovieSchema
from app.container import movie_service
from app.helpers.decorators import admin_required, auth_required

movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = movie_service.get_all()
        return movies_schema.dump(all_movies), 200

    @admin_required
    def post(self):
        req_json = request.json
        movie_service.create(req_json)

        return "", 201


@movie_ns.route('/genre_id=<int:gid>')
class MoviesView(Resource):
    def get(self, gid: int):
        movies_filtered = movie_service.get_by_genres(gid)
        return movies_schema.dump(movies_filtered), 200


@movie_ns.route('/director_id=<did>')
class MoviesView(Resource):
    def get(self, did):
        movies_filtered = movie_service.get_by_directors(did)
        return movies_schema.dump(movies_filtered), 200


@movie_ns.route('/year=<year>')
class MoviesView(Resource):
    def get(self, year):
        movies_filtered = movie_service.get_by_year(year)
        return movies_schema.dump(movies_filtered), 200


@movie_ns.route('/<mid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid):
        movie = movie_service.get_one(mid)
        return movie_schema.dump(movie), 200

    @admin_required
    def put(self, mid):
        req_json = request.json
        req_json['id'] = mid

        movie_service.update(req_json)

        return "", 204

    @admin_required
    def patch(self, mid):
        req_json = request.json
        req_json['id'] = mid

        movie_service.update_partial(req_json)

        return "", 204

    @admin_required
    def delete(self, mid):
        movie_service.delete(mid)

        return "", 204
