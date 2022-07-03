# Casting Agency API

The Casting Agency models a company that is responsible for creating movies and actors. You are an Producer within the company and are creating a system to simplify and streamline your process.

This project uses python, flask and postgresql for it's backend and is hosted on Heroku.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/)

No frontend is developed for this app, you can use it using cURL or [Postman](https://www.postman.com)

<a name="motivation"></a>
## Motivations & Covered Topics

This is the last project of the `Udacity-Full-Stack-Nanodegree` Course.
It covers following technical topics in 1 app:

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization & Role based Authentification with `Auth0` (see `auth.py`)
5. Deployment on `Heroku`

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


#### Virtual Enviornment

Instructions for setting up a virtual environment can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we use to handle cross origin requests from the frontend server.

## Running the server

First ensure that you are working in the created virtual environment.

To run the server, execute:

```bash
source setup.sh
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
Sourcing `setup.sh` sets some environment variables used by the app.

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the this file to find the application.

You can run this API locally at the default `http://127.0.0.1:5000/`

Login url `https://casting-agency-full-stack.us.auth0.com/authorize?audience=casting-agency-full-stack&response_type=token&client_id=05PDUxQbk8GV2eLEfOJlsC58sDxefb1D&redirect_uri=http://localhost:5000/callback`

## Testing

To run the tests,

Create user "agency" with the command 
```
createuser agency
```
Create database with the command 
```
createdb agency_test
```
If database already exist run the following command to drop the database and recreate it
```
dropdb agency_test && createdb agency_test
```
Run the dump file with the command 
```
psql agency_test < agency.psql
```
Run the test suits with the command
```
python test_app.py
```

## Deployment

The app is deployed on Heroku [https://capstonealisha.herokuapp.com/](https://capstonealisha.herokuapp.com/)

Auth0 information for endpoints that require authentication can be found in setup.sh

## API Reference

### Getting Started

- Base URL: [https://capstonealisha.herokuapp.com/](https://casting-agency-full-stack.herokuapp.com/)
- Authentication: This app has 3 users. Each has his own token which are provided in `setup.sh` file. Details about each user privilege are provided below.

### Users

This app has 3 users. each user has his own privileges.

- Associate
	- Can view actors and movies

- Director
	- All permissions of a Casting Assistant and…
	- Add or delete an actor from the database
	- Modify actors or movies

- Producer
	- All permissions of a Casting Director and…
	- Add or delete a movie from the database

### How to Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `delete:actors`
    - `delete:movies`
    - `get:actors`
    - `get:movies`
    - `patch:actors`
    - `patch:movies`
    - `post:actors`
    - `post:movies`
6. Create new roles for:
    - Associate
	    - Can view actors and movies
    - Director
	    - All permissions of a Associate and…
	    - Add or delete an actor from the database
	    - Modify actors or movies
    - Producer
	    - All permissions of a Director and…
	    - Add or delete a movie from the database
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 3 users - assign the Associate role to one, Director role to the second and Producer role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `capstone.postman_collection.json`
    - Right-clicking the collection folder for Associate,Director and Producer, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection.
    - Export the collection overwriting the one we've included so that we have proper JWTs

## Testing

I used `Postman Collections` to test all my Endpoints for expected behaviour & correct permission execution.

To execute the tests, follow these steps:

1. Install [Postman](https://www.getpostman.com/downloads/)
2. Download the json file from this repository (`capstone.postman_collection.json`)
3. Open `Postman` and click on "Import" on the top-left corner
4. Select `capstone.postman_collection.json`
5. Once uploaded, Click on "Runner"

### Endpoints

- GET '/actors'
- GET '/movies'
- POST '/actors'
- POST '/movies'
- PATCH '/actors/<int:id>'
- PATCH '/movies/<int:id>'
- DELETE '/actors/<int:id>'
- DELETE '/movies/<int:id>'

Following is the demonstration of each endpoint.

- GET '/actors'
	- Fetch all Actor info from DB
	- Request Argument : None
	- Returns : JSON response containing all actors with their info, and request status
	- example
		```
		{
        "actors": [
            {
            "age": "26",
            "gender": "male",
            "id": 8,
            "name": "Kiki"
            }
        ],
		  "success": true
		}
		```

- GET '/movies'
	- Fetch all Movies info from DB
	- Request Argument : None
	- Returns : JSON response containing all movies with their info, and request status
	- example
		```
		{
        "movies": [
            {
            "id": 7,
            "release": "2019",
            "title": "actor1"
            }
        ],
        "success": true
        }
		```

- POST '/actors'
	- Insert Actor info into DB
	- Request Argument :  
    ```
        {
        "name":"Reyan", 
        "age":20, 
        "gender":"male"
        }
    ```
	- Returns : JSON response containing request status
	- example
		```
		{
        "actor": {
            "age": "20",
            "gender": "male",
            "id": 51,
            "name": "Reyan"
        },
        "success": true
        }
		```

- POST '/movies'
	- Insert Movie info into DB
	- Request Argument : 
    ```
        {
        "title":"TheEnd2020", 
        "release":2021
        }
    ```
	- Returns : JSON response containing request status
	- example
		```
		{
        "actor": {
            "id": 36,
            "title":"TheEnd2020", 
            "release":2021
        },
        "success": true
        }
		```

- PATCH '/actors/<int:id>'
	- Updtae Actor info and insert it DB
	- Request Argument : 
    ```
        {
        "age":21
        }
    ```
	- Returns : JSON response containing request status
	- example
		```
		{
        "actor": {
            "age": "21",
            "gender": "male",
            "id": 51,
            "name": "Reyan"
        },
        "success": true
        }
		```

- PATCH '/movies/<int:id>'
	- Updtae Movie info and insert it DB
	- Request Argument : 
    ```
        {
        "release":2022
        }
    ```
	- Returns : JSON response containing request status
	- example
		```
		{
        "actor": {
            "id": 36,
            "title":"TheEnd2020", 
            "release":2022
        },
        "success": true
        }
		```

- DELETE '/actors/<int:id>'
	- Delete Actor from DB
	- Request Argument : None
	- Returns : JSON response containing request status
	- example
		```
		{
        "id": 9,
        "success": true
        }
		```

- DELETE '/movies/<int:id>'
	- Delete Movie from DB
	- Request Argument : None
	- Returns : JSON response containing request status
	- example
		```
		{
        "id": 10,
        "success": true
        }
		```
