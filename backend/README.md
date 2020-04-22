# Full Stack Trivia API Backend

###description
Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

Here under this project we are building the API's for Trivia App.
Under this project all API's will be called from Trivia App front end and every request for questions, categories etc will be served to the front end.

#####Code Style
This project adheres to the python [PEP8](https://www.python.org/dev/peps/pep-0008/) Coding guidelines.


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

## API Reference
- **Base URL**: At present this app can only be run locally. The backend app is hosted at the 
default, ```http://127.0.0.1:5000/```, which is set as a proxy to front end configuration.
- **Authentication**: This version of the application does not require authentication or API keys.

### Error Handling
Error handling are returned as JSON Objects in the below mentioned format.
```
{
  "error": 404,
  "message": "Request resource not found",
  "success": false
}
```
The API will return 3 types of error if request fails / for invalid requests:
- 404: Not Found
- 422: Unprocessable Entity
- 405: Method not allowed

### API Endpoints

#### GET /categories
- General: Return list of all Question category
- Sample: ```curl http://127.0.0.1:5000/categories```
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
  "success": true
}
```
#### GET /questions
- General: Return list of question objects, success value, and total number of questions along with category metadata.
Default 10 questions will be returned per page.
- Sample: ```curl http://127.0.0.1:5000/questions```
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
  "page": 1,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 23
}
```
#### POST /questions/search
- General: Return list of question objects, success value, and total number of questions based on provided search string
 along with category metadata.
- Sample: ``` curl -X POST http://127.0.0.1:5000/questions/search -d '{ "searchTerm": "Full stack"}' ```
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
  "questions": [
    {
      "answer": "udacity",
      "category": "1",
      "difficulty": 1,
      "id": 27,
      "question": "From where we can learn Full stack development course?"
    },
    {
      "answer": "udacity",
      "category": "1",
      "difficulty": 1,
      "id": 28,
      "question": "From where we can learn Full stack development course?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

#### DELETE /questions/{question_id}
- General: Deletes the question from database and returns success in response.
- Sample: ``` curl -X DELETE http://127.0.0.1:5000/questions/24 ```
```
{
  'success': true,
  'message': Question ID 24 has been deleted'
}
```

#### POST /questions
- General: Creates a question in system.
- Sample: ``` curl -X POST http://127.0.0.1:5000/questions/24 -d '{"question": "which country bangalore is present?","answer": "India","difficulty": 1,"category": 1}' ```
```
{
  'success': true,
}
```

#### GET /categories/{category_id}/questions
- General: search all questions based on the category id and return in response
- Sample: ``` curl POST http://127.0.0.1:5000/categories/24/questions/```
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
  "page": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "India",
      "category": "1",
      "difficulty": 1,
      "id": 25,
      "question": "which country bangalore is present?"
    },
    {
      "answer": "udacity",
      "category": "1",
      "difficulty": 1,
      "id": 27,
      "question": "From where we can learn Full stack development course?"
    },
    {
      "answer": "udacity",
      "category": "1",
      "difficulty": 1,
      "id": 28,
      "question": "From where we can learn Full stack development course?"
    }
  ],
  "success": true,
  "total_questions": 6
}
```

#### POST /quizzes
- General: Return One Question randomly based on the id provided. if Id is 0 or null, questions from all categories will be served
- Sample: ``` curl curl --request POST 'http://127.0.0.1:5000/quizzes' --data-raw '{"previous_questions": [],"quiz_category": {"type": "Science","id": "1"}}'```
```
{
  "question": {
    "answer": "The Liver",
    "category": "1",
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```
## Testing
To run the tests, run
```
CREATE DATABASE trivia_test 
WITH TEMPLATE trivia;
psql trivia_test < trivia.psql
python test_flaskr.py
```

##Author
####Ravi Kumar

##Acknowledgements
#### [Udacity](http://udacity.com/) 