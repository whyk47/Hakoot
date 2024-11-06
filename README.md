# Hakoot - Django Web App

Hakoot is a Django web application for creating and playing quizzes. Users can create quizzes, answer questions, and view their scores. The application supports features such as user authentication, quiz creation, editing, and deletion, as well as quiz playing and scoring.

## Table of Contents
- [Video Demo](#video-demo)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Distinctiveness and Complexity](#distinctiveness-and-complexity)


## Video Demo
[Click to play](https://www.youtube.com/watch?v=61no9QvlWX8)


## Installation
1. Clone the repository
   ```bash
   git clone https://github.com/whyk47/Hakoot.git
   ```
2. Start the development server with the following batch command.
   ```bash
   ./run
   ```
3. You should get the following output.
   ```bash
      $ python manage.py runserver
      Watching for file changes with StatReloader
      Performing system checks...

      System check identified no issues (0 silenced).
      November 06, 2024 - 20:03:07
      Django version 5.0.4, using settings 'hakoot.settings'
      Starting development server at http://127.0.0.1:8000/
      Quit the server with CTRL-BREAK.
   ```
Follow the link to the development server to access the application.

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