import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def get_all_categories():
    categories = Category.query.all()
    sorted = {category.id: category.type for category in categories}
    return sorted


def paginate_ques(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = list(map(Question.format, selection))
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories')
    def get_categories():
        categories = get_all_categories()
        if len(categories) == 0:
            abort(404)
        result = {
            'success': True,
            'categories': categories
        }

        return jsonify(result)

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_ques = paginate_ques(request, questions)
        categories = get_all_categories()

        if len(questions) == 0:
            abort(404)

        result = {
            'success': True,
            'questions': current_ques,
            'total_questions': len(questions),
            'categories': categories,
            'current_category': None,
            'page': request.args.get('page', 1, type=int)
        }

        return jsonify(result)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question_by_id(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).first()
            print(question)
            question.delete()
        except:
            abort(404)
        finally:
            result = {
                'success': True,
                'message': f'Question ID {question_id} has been deleted'
            }
        return jsonify(result)

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        question = Question(question=body['question'], answer=body['answer'],
                            category=body['category'],
                            difficulty=body['difficulty'])
        question.insert()

        result = {
            'success': True
        }

        return jsonify(result)

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions/search', methods=['POST'])
    def search_for_question():
        try:
            search_term = request.get_json()['searchTerm']
        except KeyError:
            abort(422)
        selection = Question.query.filter(Question.question.like(f'%{search_term}%')).all()
        ques_list = [ques.format() for ques in selection]
        categories = get_all_categories()

        if len(ques_list) == 0:
            abort(404)

        result = {
            'success': True,
            'questions': ques_list,
            'total_questions': len(ques_list),
            'categories': categories
        }
        return jsonify(result)

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_specified_by_category(category_id):
        questions = Question.query.filter_by(category=str(category_id)).all()
        current_question = paginate_ques(request, questions)
        categories = get_all_categories()

        if len(current_question) == 0:
            abort(404)

        result = {
            'success': True,
            'questions': current_question,
            'total_questions': len(questions),
            'categories': categories,
            'page': request.args.get('page', 1, type=int)

        }
        return jsonify(result)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        if body['quiz_category']['id'] == 0:
            selection = Question.query.all()
        else:
            selection = Question.query.filter_by(category=body['quiz_category']['id']).all()
        questions = list(map(Question.format, selection))

        if len(questions) == 0:
            abort(404)

        for question in body['previous_questions']:
            questions = list(filter(lambda i: i['id'] != question, questions))

        if questions:
            question = random.choice(questions)
        else:
            question = False

        result = {
            'success': True,
            'question': question
        }
        return jsonify(result)

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": "Request resource not found"
            }
        ), 404

    '''App Error Handlers to send error response in json format'''

    @app.errorhandler(422)
    def unprocessable_entiry(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "Unprocessable Entity"
            }
        ), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(
            {
                "success": False,
                "error": 405,
                "message": "Method not allowed"
            }
        ), 405

    return app
