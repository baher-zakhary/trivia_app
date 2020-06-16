# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Documentation

Endpoints

**GET '/api/categories'**
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with keys
	- categories, that contains a object of id: category_string key:value pairs. 
	- success, that contains a boolean to indicate success or failure status
	- total, that states the total number of categories returned
```
{
"categories": {
"1": "Science", 
"2": "Art", 
"3": "Geography", 
"4": "History", 
"5": "Entertainment", 
"6": "Sports"
},
"success": true, 
"total": 6
}
```
    
**GET '/api/questions'**
- Fetches a list of questions per page and a dictionary of all categories in which the keys are the ids and the value is the 		   corresponding string of the category
- Request Arguments:
	- page: query parameter with a value equals to required page of questions
- Returns: An object with keys
	- questions, an array of question objects in requested page
	- categories, that contains a object of id: category_string key:value pairs. 
	- success, that contains a boolean to indicate success or failure status
	- total_questions, that states the total number of categories returned
```
{
"categories": {
"1": "Science", 
"2": "Art", 
"3": "Geography", 
"4": "History", 
"5": "Entertainment", 
"6": "Sports"
}, 
"current_category": null, 
"questions": [
{
"answer": "Tom Cruise", 
"category": 5, 
"difficulty": 4, 
"id": 4, 
"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
}, 
], 
"success": true, 
"total_questions": 20
}
```

**DELETE '/api/questions/{id}'**
- Deletes a question with the provided ID
- Request Arguments:
	- id: route parameter of the id of the question to be deleted
- Returns: An object with keys
	- success, that contains a boolean to indicate success or failure status
```
{
  "success": true
}
```

**POST '/api/questions' (For searching for questions)**
- searches for questions containing the search term
- Request Arguments:
	- searchTerm: the term to search by for questions
- Returns: An object with keys
	- questions, an array of question objects in that contains the search term
	- success, that contains a boolean to indicate success or failure status
	- total_questions, that states the total number of categories returned
```
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

**POST '/api/questions' (For adding a question)**
- Adds a new question
- Request Arguments:
	- answer:  the answer of the question
	- category:  the category of the question
	- difficulty:  its difficulty
	- question:  the question
- Returns: An object with keys
	- success, that contains a boolean to indicate success or failure status
```
{
  "success": true
}
```

**GET '/api/categories/{category_id}/questions'**
- Fetches a list of questions in a certain category
- Request Arguments:
	- category_id: route parameter specifies the category ID
- Returns: An object with keys
	- questions, an array of question objects in requested category
	- current_category, the id of the requested category
	- success, that contains a boolean to indicate success or failure status
	- total_questions, that states the total number of categories returned
```
{
  "current_category": 3, 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

**POST '/api/quizzes'**
- Gets a random question from the selected category to play quizzes game
- Request Arguments:
	- previous_questions, takes a list of previous questions IDs as to not repeat a question that was previously answered
	- quiz_category, takes an object with two keys
			-	type, the string type of a category
			-	id, the int id of a category
- Returns: An object with keys
	- question, the next random question object in the current quiz game
	- success, that contains a boolean to indicate success or failure status
```
{
  "question": {
    "answer": "Orange :D", 
    "category": 1, 
    "difficulty": 1, 
    "id": 24, 
    "question": "What is the color of Oranges ?"
  }, 
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
