# Hakoot - Django Web App

Hakoot is a Django web application for creating and playing quizzes. Users can create quizzes, answer questions, and view their scores. The application supports features such as user authentication, quiz creation, editing, and deletion, as well as quiz playing and scoring.

## Table of Contents
- [Video Demo](#video-demo)
- [Distinctiveness and Complexity](#distinctiveness-and-complexity)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)

## Video Demo
[Click to play](https://www.youtube.com/watch?v=61no9QvlWX8)

## Distinctiveness and Complexity

1. **Dynamic Question Addition/Removal:**
   - The project allows dynamic addition and removal of quiz questions on the create and edit quiz page. This is achieved through client-side JavaScript (`create.js`), enhancing the user experience by enabling them to modify the quiz structure interactively.

2. **Asynchronous Communication:**
   - The play page (`play.js`) demonstrates asynchronous communication with the server using the Fetch API. It submits answers, marks the question and retrieves the leaderboard without refreshing the entire page, providing a seamless and efficient quiz-taking experience.

3. **Responsive Design:**
   - The play page features a real-time timer for each question. The timer dynamically updates, providing users with a visual representation of the time remaining to answer a question. The timer also triggers automatic submission if time runs out. In addition, the timer does not reset even when the page is refreshed, as the start time is stored in local storage.
   - Upon clicking an option, the play page dynamically updates to show the result of the player's answer. A button also appears to allow the user to proceed with the next question.
   - After completing the quiz, the user is presented with a leaderboard (`play.js`) showcasing the scores of the player's score and up to 5 other top scores. This leaderboard is also displayed and updated on the view quiz page.
   - The index page features pagination and search functions, allowing the user the easily navigate to any quiz.

4. **Aesthetics:**
    - The project makes use of many different bootstrap elements (eg. cards, list-groups, buttons) to achieve a sleek and aesthetically pleasing design. In particular, there is apt use of margins to space DOM elements appropriately.

## Installation

1. Clone the repository

2. Navigate to the project directory:
   ```bash
   cd hakoot
   ```

3. Make database migrations:
   ```bash
   python manage.py makemigrations
   ```
   
5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser account for administration:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the application.

## Usage

1. Register for a new account or log in if you already have one.
2. Create a new quiz by navigating to the "Create Quiz" section.
3. Edit or delete quizzes by clicking any quiz from the "My Quizzes" section.
4. Play quizzes made by other users and view your scores on the leaderboard.
5. Log out when you are done.

## File Structure

- `views.py`: Contains the Django views for handling various functionalities such as rendering pages, creating, editing, and deleting quizzes, and playing quizzes.
- `util.py`: Contains utility functions used in the application, such as pagination.
- `models.py`: Defines the database models for User, Quiz, Question, Option, Quiz_attempt, and Question_attempt.
- `urls.py`: Configures the URL patterns for the application.
- `forms.py`: Contains Django forms for Quiz, Question, and Option.
- `templates/`: Contains HTML templates for rendering different pages.
- `static/`: Contains static files such as CSS and JavaScript.

