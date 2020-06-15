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
        self.username = "postgres"
        self.password = "0000"
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(self.username, self.password, "localhost:5432", self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        response = self.client().get('/api/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total'])

    def test_get_paginated_questions(self):
        response = self.client().get('/api/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])

    def test_get_questions_invalid_page_404(self):
        response = self.client().get('/api/question?page=-1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        response = self.client().delete('/api/questions/4')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question_404(self):
        response = self.client().delete('/api/questions/-1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    def test_add_question(self):
        new_question = {
            "question": "test_question",
            "answer": "test_question_answer",
            "difficulty": "2",
            "category": "3"
        }
        response = self.client().post('/api/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_question_400(self):
        new_question = {
            "questio": "test_question",
            "answer": "test_question_answer",
            "difficulty": "2",
            "category": "3"
        }
        response = self.client().post('/api/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_search_question(self):
        search_term = {"searchTerm": "entitled"}
        response = self.client().post('/api/questions', json=search_term)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_get_questions_by_category(self):
        response = self.client().get('/api/categories/2/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(len(data['questions']))

    def test_get_questions_by_category_404(self):
        response = self.client().get('/api/categories/-1/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_quizzes(self):
        quizzes_req_body = {
            "previous_questions":[],
            "quiz_category": {"type": "Art", "id": "2"}
        }
        response = self.client().post('/api/quizzes', json=quizzes_req_body)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()