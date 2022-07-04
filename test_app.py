import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import Actor, Movie, setup_db
import random
import string

def random_key(length):
	key = ''
	for i in range(length):
		key += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
	return key
    

class CapstoneTest(unittest.TestCase):
    def setUp(self):
        self.token_assistant = os.environ['associate_token']
        self.token_director = os.environ['director_token']
        self.token_producer = os.environ['producer_token']
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://postgres:password@localhost:5432/agency_test"
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_Unauthorized_Permission_NO_HEADERS_get_Actors(self):
        res = self.client().get('/actors')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_get_Actors(self):
        res = self.client().get('/actors', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_404_wrong_endpoint_get_Actors(self):
        res = self.client().get('/actorss', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_get_Movies(self):
        res = self.client().get('/movies', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_404_wrong_endpoint_get_Movies(self):
        res = self.client().get('/move', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_delete_Actor(self):
        actor = Actor.query.first()
        res = self.client().delete('/actors/'+ str(actor.id), headers={
            "Authorization": 'bearer '+self.token_producer})
        body = json.loads(res.data)
        ques = Actor.query.get(actor.id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(ques, None)

    def test_404_Wrong_ID_delete_Actor(self):
        res = self.client().delete('/actors/100', headers={
            "Authorization": 'bearer '+self.token_producer})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_401_Unauthorized_Permission_delete_Actor(self):
        res = self.client().delete('/actors/1', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_delete_Movie(self):
        movie = Movie.query.first()
        res = self.client().delete('movies/'+ str(movie.id), headers={
            "Authorization": 'bearer '+self.token_producer})
        body = json.loads(res.data)
        ques = Movie.query.get(movie.id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(ques, None)

    def test_404_Wrong_ID_delete_Movies(self):
        res = self.client().delete('/movies/100', headers={
            "Authorization": 'bearer '+self.token_producer})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_Unauthorized_Permission_delete_Movies(self):
        res = self.client().delete('/movies/1', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_create_Actor(self):
        res = self.client().post(
            '/actors',
            json={
                "name": "Actor"+random_key(5),
                "age": "10",
                "gender": "Male"},
            headers={"Authorization": 'bearer '+self.token_director}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_400_wrong_Movie_ID_create_Actor(self):
        res = self.client().post(
            '/actors',
            json={
                "name": random_key(5),
                "age": "1",},
            headers={"Authorization": 'bearer '+self.token_director}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(body['success'], False)

    def test_401_Unauthorized_Permission_create_Actor(self):
        res = self.client().post(
            '/actors',
            json={
                "name": random_key(5),
                "age": "1",
                "gender": "Male"},
            headers={"Authorization": 'bearer '+self.token_assistant}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_create_Movie(self):
        res = self.client().post(
            '/movies',
            json={
                "title": "Movie"+random_key(5),
                "release": "2012"},
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_400_wrong_Actor_ID_create_Movie(self):
        res = self.client().post(
            '/movies',
            json={
                "titletr": random_key(5),
                "release": "2012"},
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(body['success'], False)

    def test_401_Unauthorized_Permission_create_Movie(self):
        res = self.client().post(
            '/movies',
            json={
                "title": random_key(5),
                "release": "2012"},
            headers={"Authorization": 'bearer '+self.token_assistant}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_update_Movies(self):
        movie = Movie.query.first()
        res = self.client().patch(
            '/movies/'+ str(movie.id),
            json={
                "title": "Title"+random_key(5),
                "release": "2012"},
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_404_wrong_ID_update_Movies(self):
        res = self.client().patch(
            '/movies/1000',
            json={
                "title": random_key(5),
                "release": "2012"},
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_401_Unauthorized_Permission_update_Movies(self):
        res = self.client().patch(
            '/movies/100',
            json={
                "title": random_key(5),
                "release": "2012"},
            headers={"Authorization": 'bearer '+self.token_assistant}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_update_Actors(self):
        actor = Actor.query.first()
        res = self.client().patch(
            '/actors/'+ str(actor.id),
            json={
                "name": "Actor"+random_key(5),
                "age": "1",
                "gender": "Male"},
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_404_wrong_ID_update_Actors(self):
        res = self.client().patch(
            '/actors/1000',
            json={
                "name": random_key(5),
                "age": "1",
                "gender": "Male"},
            headers={"Authorization": 'bearer '+self.token_producer}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)


if __name__ == "__main__":
    unittest.main()