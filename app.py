# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import click
import json
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import unittest
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from database.models import Actor, Movie, setup_db
from auth.auth import *
ROWS_PER_PAGES = 12


def paginate_row_results(request, selection):
        page = request.args.get('page', 1, type=int)
        start_page =  (page - 1) * ROWS_PER_PAGES
        end_page = start_page + ROWS_PER_PAGES
        objects_formatted = [object_name.format() for object_name in selection]
        return objects_formatted[start_page:end_page]

def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def welcome():
        msg = 'Welcome to the Casting Agency'
        return jsonify(msg)

    # GET List of Actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors_list(payload):
        actors_list = Actor.query.all()
        if not actors_list:
            abort(404)
        actors_ordered = paginate_row_results(request, actors_list)
        return jsonify({
            'actors': actors_ordered,
            'success': True
        }), 200

    # GET List of movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies_list(payload):
        movies_list = Movie.query.all()
        if not movies_list:
            abort(404)
        movies_ordered = paginate_row_results(request, movies_list)
        return jsonify({
            'movies': movies_ordered,
            'success': True
        }), 200
    
    # Create actor 
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def insert_actor(payload):
        data = request.get_json()
        if data is None:
            abort(400)
        name = data.get('name') or None
        age = data.get('age') or None
        gender = data.get('gender') or None
        if ((name is None) or (age is None) or (gender is None)):
            abort(400)
        new_actor = Actor(name=name, age=age, gender=gender)
        try:
            new_actor.insert()
        except Exception as e:
            abort(422)
        return jsonify({
            'actor': new_actor.format(),
            'success': True
        }), 200

    # Create movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def insert_movie(payload):
        data = request.get_json()
        if data is None:
            abort(400)
        title = data.get('title') or None
        release = data.get('release') or None
        if ((title is None) or (release is None)):
            abort(400)
        new_movie = Movie(title=title, release=release)
        try:
            new_movie.insert()
        except Exception as e:
            abort(422)
        return jsonify({
            'movie': new_movie.format(),
            'success': True           
        }), 200

    # Update actor
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_selected_actor(payload, id):
        if not id:
            abort(404)
        selected_actor = Actor.query.get(id)
        if not selected_actor:
            abort(404)
        data = request.get_json()
        if data is None:
            abort(400)
        if 'name' in data:
            selected_actor.name = data['name']
        if 'age' in data:
            selected_actor.age = data['age']
        if 'gender' in data:
            selected_actor.gender = data['gender']
        selected_actor.update()
        return jsonify({
            'actor': selected_actor.format(),
            'success': True
        }), 200

    # Update movie
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_selected_movie(payload, id):
        if not id:
            abort(404)
        selected_movie = Movie.query.get(id)
        if not selected_movie:
            abort(404)
        data = request.get_json()
        if 'title' in data:
            selected_movie.title = data['title']
        if 'release' in data:
            selected_movie.release = data['release']
        selected_movie.update()
        return jsonify({
            'movie': selected_movie.format(),
            'success': True            
        }), 200

    # DELETE actor
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_selected_actor(payload, id):
        if not id:
            abort(404)
        selected_actor = Actor.query.get(id)
        if not selected_actor:
            abort(404)
        selected_actor.delete()
        return jsonify({
            'actor_id': id,
            'success': True            
        }), 200

    # DELETE movie
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_selected_movie(payload, id):
        if not id:
            abort(404)
        selected_movie = Movie.query.get(id)
        if not selected_movie:
            abort(404)
        selected_movie.delete()
        return jsonify({
            'movie_id': id,
            'success': True            
        }), 200

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app

app = create_app()