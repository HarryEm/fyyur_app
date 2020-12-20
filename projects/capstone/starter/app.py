import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def hello_world():
      return 'Hello, World from Flask!\n'

  @app.route('/actors', methods=['GET'])
  def get_actors():
    actors = [actor.format() for actor in Actor.query.all()]
    return jsonify({
              "success": True,
              'status_code': 200,
              "actors": actors
            }), 200

  @app.route('/movies', methods=['GET'])
  def get_movies():
    movies = [movie.format() for movie in Movie.query.all()]
    return jsonify({
              "success": True,
              'status_code': 200,
              "movies": movies
            }), 200

  @app.route('/actors', methods=['POST'])
  def create_actor():
    body = request.get_json()
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')

    actor = Actor(name=name, age=age, gender=gender)

    actor.insert()

    return jsonify({
                "success": True,
                'status_code': 200
            }), 200

  @app.route('/movies', methods=['POST'])
  def create_movie():
    body = request.get_json()
    title = body.get('title')
    release_date = body.get('release_date')

    movie = Movie(title=title, release_date=release_date)

    movie.insert()

    return jsonify({
                "success": True,
                'status_code': 200
            }), 200

  @app.route('/actors/<int:id>', methods=['PATCH'])
  def edit_actor(id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()

    # Check actor exists
    if not actor:
        abort(404)

    body = request.get_json()
    actor.name = body.get('name', actor.name)
    actor.age = body.get('age', actor.age)
    actor.gender = body.get('gender', actor.gender)

    actor.update()

    return jsonify({
                "success": True,
                'status_code': 200
            }), 200

  @app.route('/movies/<int:id>', methods=['PATCH'])
  def edit_movie(id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    # Check actor exists
    if not movie:
        abort(404)

    body = request.get_json()
    movie.title = body.get('title', movie.title)
    movie.release_date = body.get('release_date', movie.release_date)

    movie.update()

    return jsonify({
                "success": True,
                'status_code': 200
            }), 200

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  def delete_actor(actor_id):
    pass

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  def delete_movie(movie_id):
    pass

  return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
