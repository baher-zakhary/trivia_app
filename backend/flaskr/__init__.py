import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import and_

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @ Set up CORS. Allow '*' for origins. Delete the sample route after
     completing the TODOs
    '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
     @ Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, DELETE, PATCH, OPTIONS')
        return response

    def paginate(page, total, page_size=QUESTIONS_PER_PAGE):
        start = (page - 1) * page_size
        end = start + page_size
        if end > total:
            end = total
        return start, end

    '''
    @: Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)
        else:
            response = {}
            for category in categories:
                response[category.id] = category.type

            return jsonify({
                "categories": response,
                "success": True,
                "total": len(response)
            })

    '''
    @: Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for
    three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/api/questions', methods=['GET'])
    def get_questions():
        questionsRes = Question.query.order_by(Question.id).all()
        categoriesRes = Category.query.order_by(Category.id).all()
        if len(questionsRes) == 0 or len(categoriesRes) == 0:
            abort(404)
        categories = {}
        for category in categoriesRes:
            categories[category.id] = category.type
        total = len(questionsRes)
        response = {
            'questions': [],
            'total_questions': total,
            'categories': categories,
            'current_category': None,
            'success': True
        }
        page = request.args.get('page', 1, type=int)
        start, end = paginate(page, total)
        for i in range(start, end):
            response['questions'].append(questionsRes[i].format())
        if len(response['questions']) == 0:
            abort(404)

        return jsonify(response)

    '''
    @: Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will
    be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/api/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).first()
            if question is None:
                abort(404)
            else:
                question.delete()
        except Exception:
            abort(500)
        return jsonify({"success": True})

    '''
    @: Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the
    last page
    of the questions list in the "List" tab.
    '''
    @app.route('/api/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        searchTerm = body.get('searchTerm', None)
        if searchTerm is not None:
            try:
                searchResult = Question.query.filter(
                    Question.question.ilike(f'%{searchTerm}%')).all()
                return jsonify({
                    "questions": [res.format() for res in searchResult],
                    "total_questions": len(searchResult),
                    "current_category": None,
                    "success": True
                })
            except Exception:
                abort(422)
        else:
            try:
                question = body.get('question', None)
                answer = body.get('answer', None)
                difficulty = body.get('difficulty', None)
                category_id = body.get('category', None)
            except Exception:
                abort(422)
            if (question is None or answer is None or difficulty is None
               or category_id is None):
                abort(400)
            try:
                new_question = Question(
                    question=question,
                    answer=answer,
                    category_id=category_id,
                    difficulty=difficulty)
                new_question.insert()
            except Exception:
                abort(422)
            return jsonify({"success": True})

    '''
  @: Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    # SEE QUESTIONS POST ENDPOINT
    '''
  @: Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/api/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        questions = Question.query.filter(
            Question.category_id == category_id).all()
        if len(questions) == 0:
            abort(404)
        else:
            return jsonify({
                "questions": [question.format() for question in questions],
                "total_questions": len(questions),
                "current_category": category_id,
                "success": True
            })

    '''
  @: Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/api/quizzes', methods=['POST'])
    def quizzes():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', [])
            quiz_category = body.get('quiz_category', None)
            if quiz_category['id'] == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(and_(
                    Question.category_id == quiz_category['id'],
                    Question.id.notin_(previous_questions))).all()

            if questions is None or len(questions) == 0:
                return jsonify({
                    "success": True,
                    "question": None
                })
            else:
                random.seed()
                question = random.choice(questions)
                return jsonify({
                    "success": True,
                    "question": question.format()
                })
        except Exception:
            abort(422)

    '''
  @: Create error handlers for all expected errors
  including 404 and 422.
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    return app
