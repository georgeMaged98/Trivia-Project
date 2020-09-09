import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app)

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response
    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''

    @app.route('/categories')
    def get_all_categories():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]
        return jsonify({
            "sucess": True,
            "categories": formatted_categories,
        })

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
    def get_all_questions():
        page = request.args.get('page', 1, type=int)
        questions = Question.query.paginate(page, 10, error_out=True).items
        categoties = Category.query.all()
        formatted_questions = [question.format() for question in questions]
        formatted_categories = [category.format() for category in categoties]
        return jsonify({
            "sucess": True,
            "total_questions": Question.query.count(),
            "questions": formatted_questions,
            "categories": formatted_categories,
            "current_category": "science"
        })
    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify({
                "success": True
            })
        except:
            abort(422)
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
        try:
            data = request.get_json()
            question = Question(data['question'], data['answer'],
                                data['category'], data['difficulty'])
            question.insert()
            return jsonify({
                "success": True
            })
        except:
            abort(422)
    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/search', methods=['POST'])
    def search_for_questions():
        request_body = request.get_json()
        if not 'search_term' in request_body:
            abort(400)
        searchTerm = request_body['search_term']
        questions = Question.query.filter(
            Question.question.ilike(f"%{searchTerm}%")).all()
        formatted_questions = [question.format() for question in questions]
        return jsonify({
            "questions": formatted_questions,
            "totalQuestions": len(formatted_questions),
            "currentCategory": "art"
        })
    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        questions = Question.query.filter(
            Question.category == category_id).all()
        formatted_questions = [question.format() for question in questions]
        current_category = Category.query.get(category_id).format()
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]
        return jsonify({
            "success": True,
            "currentCategory": current_category,
            "totalQuestions": len(formatted_questions),
            "questions": formatted_questions
        })
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
    def play():
        previous_questions = request.get_json()['previous_questions']
        quiz_category_id = request.get_json()['quiz_category']['id']

        if len(previous_questions) == 5:
            return jsonify({
                "success": True,
            })
        if quiz_category_id == 0:
            questions = Question.query.all()
            questions_ids = [question.format()['id'] for question in questions]
            for q in previous_questions:
                questions_ids.remove(q)
            if len(questions_ids) == 0:
                return jsonify({
                    "success": True,
                })
            array_index = random.randint(0, len(questions_ids))
            question_id = questions_ids[array_index]
            return jsonify({
                "success": True,
                "question": Question.query.get(question_id).format()
            })
        else:
            category = Category.query.filter(
                Category.id == quiz_category_id).one_or_none()
            if category is None:
                abort(422)
            category_id = category.id
            questions = Question.query.filter(
                Question.category == quiz_category_id).all()
            questions_ids = [question.format()['id'] for question in questions]
            for q in previous_questions:
                questions_ids.remove(q)
            if len(questions_ids) == 0:
                return jsonify({
                    "success": True,
                })
            array_index = random.randint(0, len(questions_ids))
            question_id = questions_ids[array_index-1]
            return jsonify({
                "success": True,
                "question": Question.query.get(question_id).format()
            })
      #   '''
      # @TODO:
      # Create error handlers for all expected errors
      # including 404 and 422.
      # '''

    @app.errorhandler(404)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(400)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(405)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    return app
