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
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:postgres@localhost:5432/trivia_test"

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_post_question_success(self):
        new_question = {
            "question": "What is the capital of USA?",
            "answer": "Washington DC",
            "difficulty": "2",
            "category": "1"
        }

        res = self.client.post('/questions', json=new_question)
        questions = Question.query.all()
        self.assertTrue(
            any([question.question == new_question['question'] for question in questions]))
        self.assertEqual(res.status_code, 200)

    # Test without the answer to the question
    def test_post_question_fail(self):
        new_question = {
            "question": "What is the capital of USA?",
            "difficulty": "2",
            "category": "1"
        }

        res = self.client.post('/questions', json=new_question)
        # print(res.status_code)
        self.assertEqual(res.status_code, 422)

    def test_get_questions_in_category_success(self):
        category = Category.query.first().id
        res = self.client.get('/categories/{}/questions'.format(category))
        self.assertEqual(res.status_code, 200)

    # Get questions of a category that is not in the database
    def test_get_questions_in_category_fail(self):
        category = 1000000
        res = self.client.get('/categories/{}/questions'.format(category))
        self.assertEqual(res.status_code, 404)

    def test_delete_question_success(self):
        question = Question.query.first().id
        res = self.client.delete('/questions/{}'.format(question))
        questions = Question.query.all()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(not
                        any([question.id == question for question in questions]))

    # Deleting non-existing question
    def test_delete_question_success(self):
        question = 51648461
        res = self.client.delete('/questions/{}'.format(question))
        questions = Question.query.all()
        self.assertEqual(res.status_code, 422)

    def test_get_all_questions_success(self):
        page_number = 1
        res = self.client.get('/questions?page={}'.format(page_number))
        self.assertEqual(res.status_code, 200)

    # Testing with a very large page number
    def test_get_all_questions_fail(self):
        page_number = 10000000
        res = self.client.get('/questions?page={}'.format(page_number))
        self.assertEqual(res.status_code, 404)

    def test_play_quiz_success(self):
        category_id = 0  # All Categories
        body = {
            "previous_questions": [],
            "quiz_category": {"id": category_id, "type": "click"}
        }
        res = self.client.post('/quizzes', json=body)
        self.assertEqual(res.status_code, 200)

    # Test with a category that is not in the database
    def test_play_quiz_fail(self):
        category_id = 120251564  # All Categories
        body = {
            "previous_questions": [],
            "quiz_category": {"id": category_id, "type": "click"}
        }
        res = self.client.post('/quizzes', json=body)
        self.assertEqual(res.status_code, 422)

    def test_get_categories_success(self):
        res = self.client.get('/categories')
        self.assertEqual(res.status_code, 200)

    # Hitting wrong URL
    def test_get_categories_fail(self):
        res = self.client.get('/categoriessssss')
        self.assertEqual(res.status_code, 404)

    def test_search_success(self):
        body = {
            "search_term": "what"
        }
        res = self.client.post('/search', json=body)
        self.assertEqual(res.status_code, 200)

    # Not Providing the search_term
    def test_search_success(self):
        body = {}
        res = self.client.post('/search', json=body)
        self.assertEqual(res.status_code, 400)

    def tearDown(self):
        """Executed after reach test"""
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
