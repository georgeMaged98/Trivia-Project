# Trivia-Project
This repo contains trivia website which is the second project in Udacity Advanced Web Development Course


## Frontend Part
In the frontend drectory run the following commands
1. npm install
2. npm start

## Backend Part
### Installing Dependencies
-Inside the backend directory, run the following command
pip install -r requirements.txt

### Database Setup
- Make sure postgres is running and run the following command
psql trivia < trivia.psql



### Starting the server
- In the backend directory: run the following commands
1. export FLASK_APP=flaskr
2. export FLASK_ENV=development
3. flask run

## API Documentation

#### GET '/categories'
- Returns an array of all available categories
- Request Body: None
- Response Object: {
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        {
            "id": 2,
            "type": "Art"
        },
        {
            "id": 3,
            "type": "Geography"
        },
        {
            "id": 4,
            "type": "History"
        },
        {
            "id": 5,
            "type": "Entertainment"
        },
        {
            "id": 6,
            "type": "Sports"
        }
    ],
    "sucess": true
}


#### GET '/questions?page=1'
- Returns an array of questions in a certain page, all avaliable categories and the total number of questions
- Query Parameters: 'page':1
- Response Body: {
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        {
            "id": 2,
            "type": "Art"
        },
        {
            "id": 3,
            "type": "Geography"
        },
        {
            "id": 4,
            "type": "History"
        },
        {
            "id": 5,
            "type": "Entertainment"
        },
        {
            "id": 6,
            "type": "Sports"
        }
    ],
    "current_category": "science",
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "sucess": true,
    "total_questions": 20
}


#### GET '/categories/1/questions'
- Returns an array of questions in a certain category
- It takes the category id in the URL
- Response Object: 
{
    "currentCategory": {
        "id": 1,
        "type": "Science"
    },
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true,
    "totalQuestions": 3
}

#### DELETE '/questions/1'
- Deletes a specific question from the database
- It takes the question id in the URL
- Repsonse Object:
{
    "success": true
}

#### POST '/questions'
- Adds a new question to the databse
- Takes the question, answer, difficulty level from 1 to 6 and the category
- Request Body:
{
    "question":"What is the capital of Egypt?",
    "answer":"Cairo",
    "difficulty":1,
    "category":3
}

- Response Object: 
{
    "success": true
}

#### POST '/quizzes'
- Returns a new question that was not asked before in this quiz according to a certain category or all categories
- It takes the category of the quiz and an array of the previous questions in the request
- Request Body:
{
    "previous_questions":[],
    "quiz_category":{"type":"Science","id":"1"}
}
- Returns a question in the category mentioned in the request that is not in the previous questions
- Response Object:
{
    "question": {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
}

#### POST '/search'
- Searches in the database for a question with a certain search term
- It takes in the request body the search term
- Request Body:
{
    "search_term":"Tom Hanks"
}
- It returns an array  of questions which contain this search term and the total number of questions with this search term
- Response Object:
{
    "currentCategory": "art",
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "totalQuestions": 1
}


### Testing

- Run the following commands 
1. dropdb trivia_test
2. createdb trivia_test
3. psql trivia_test < trivia.psql
4. python test_flaskr.py
