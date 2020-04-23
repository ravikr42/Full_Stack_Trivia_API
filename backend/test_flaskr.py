import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}". \
            format('<inputdbusername>',
                   '<inputurpassword>',
                   'localhost:5432',
                   self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'From where we can learn Full '
                        'stack development course?',
            'answer': 'udacity',
            'difficulty': 1,
            'category': 1
        }

        self.search_json = {
            'searchTerm': 'Full stack'
        }

        self.quiz_json = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Science',
                'id': '1'
            }
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Done: Test cases for all endpoints & error cases.
    """

    # Test cases for testing get all categories api
    def test_get_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        # Validations
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    # Test case for testing get all questions
    def test_get_all_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        # Validations
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['page'], 1)

    # Test case for testing get all questions
    def test_get_all_questions_with_qp(self):
        response = self.client().get('/questions?page=2')
        data = json.loads(response.data)
        # Validations
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['page'], 2)

    def test_create_question(self):
        response = self.client().post('questions', json=self.new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_search_for_question_and_delete(self):
        # searching
        response = self.client().post('/questions/search',
                                      json=self.search_json)
        data = json.loads(response.data)
        id = data['questions'][0]['id']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        # deleting
        response = self.client().delete(f'questions/{id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_delete_question_invalid_id(self):
        response = self.client().delete(f'questions/999')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    def test_get_questions_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)
        # Validations
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['page'], 1)

    def test_play_quizz(self):
        response = self.client().post('/quizzes', json=self.quiz_json)
        data = json.loads(response.data)
        # Validations
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('question')

    def test_get_categories_invalid_http_method_405_scenario(self):
        response = self.client().post('/categories')
        data = json.loads(response.data)
        # Validations
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method not allowed')
        self.assertEqual(data['success'], False)

    def test_search_for_Invalid_category_id_404_scenario(self):
        response = self.client().get('/categories/1000/questions')
        data = json.loads(response.data)
        # Validations
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Request resource not found')
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
