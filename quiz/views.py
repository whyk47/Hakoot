from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
import json

from .models import *
from .forms import *
from .util import *

def index(request, username=None):
    """
    Handles the index page view for quizzes.

    Parameters:
    - request: The HTTP request object.
    - username (optional): The username of the quiz creator.

    Returns:
    - The rendered HTML response for the index page.

    Description:
    This function handles the rendering of the index page for quizzes. 
    It accepts an HTTP request object and an optional username parameter. 
    If a username is provided, the page title is set to the username, and only quizzes created by that user are displayed. 
    If no username is provided, the page title is set to "All Quizzes" and all quizzes are displayed.
    If the request method is POST, the page title is set to "Search Results" and the quizzes are filtered based on a search query provided in the request POST data.
    The function then calls the `get_page` function to paginate the quizzes and retrieve the current page. 
    Finally, it renders the `index.html` template with the page title and page object passed as context.
    """
    if username:
        page_title = username
        quizzes = Quiz.objects.filter(creator__username=username)
    else:
        page_title = "All Quizzes"
        quizzes = Quiz.objects.all()
    if request.method == "POST":
        page_title = "Search Results"
        query = str(request.POST['query']).lower()
        quizzes = quizzes.filter(name__contains=query)
    page = get_page(request, quizzes.order_by("-timestamp"))
    return render(request, "quiz/index.html", {
            "page_title": page_title,
            "page": page
        })

def view(request, quiz_id):
    """
    Renders the view for a specific quiz.

    Args:
        request (HttpRequest): The HTTP request object.
        quiz_id (int): The ID of the quiz.

    Returns:
        HttpResponse: The rendered view of the quiz.
    """
    quiz = Quiz.objects.get(id=quiz_id)
    if request.user.is_authenticated:
        quiz_attempt = Quiz_attempt.objects.filter(user=request.user, quiz=quiz).first()
    else:
        quiz_attempt = None

    all_attempts = Quiz_attempt.objects.filter(quiz=quiz).all()
    leaderboard = sorted(all_attempts, key=lambda x: x.score(), reverse=True)[:5]

    return render(request, "quiz/view.html", {
        "quiz": quiz,
        "quiz_attempt": quiz_attempt,
        "leaderboard": leaderboard

    })

@login_required
def play(request, quiz_id):
    """
    Takes a request and a quiz_id and performs the necessary actions to play a quiz.
    
    Parameters:
    - request: The request object containing information about the user and the request method.
    - quiz_id: The ID of the quiz to be played.
    
    Returns:
    - If the request method is "GET", renders the "quiz/play.html" template with the following context:
        - "quiz": The Quiz object corresponding to the quiz_id.
        - "quiz_attempt": The Quiz_attempt object created or retrieved for the current user and quiz.
        - "qns": The queryset of questions for the quiz, excluding those that the user has attempted, ordered by question number.
        - "options": The queryset of options for the quiz, ordered by question number and option number.
    - If the request method is "PUT", saves the user's chosen option and time left for the current question and returns a JsonResponse with the following data:
        - "correct_option": The correct option for the current question.
        - "score": The score calculated for the current question attempt.
    """
    quiz = Quiz.objects.get(id=quiz_id)
    quiz_attempt, created_new = Quiz_attempt.objects.get_or_create(
        user=request.user,
        quiz=quiz
    )
    if request.method == "GET":
        qn_attempts = quiz_attempt.qn_attempts.all().order_by("question__qn_no")
        return render(request, "quiz/play.html", {
            "quiz": quiz,
            "quiz_attempt": quiz_attempt,
            "qns": quiz.questions.exclude(attempts__in=qn_attempts).all().order_by("qn_no"),
            "options": quiz.options.all().order_by("qn_no", "option_no"),
        })
    elif request.method == "PUT":
        data = json.loads(request.body)
        time_left = int(data["time_left"])
        option_chosen = int(data["option_chosen"])
        qn = quiz.questions.get(qn_no=quiz_attempt.current_question())
        qn_attempt, created_new = Question_attempt.objects.get_or_create(
            question=qn,
            quiz_attempt=quiz_attempt
        )
        qn_attempt.option_chosen = option_chosen
        qn_attempt.time_left = time_left
        qn_attempt.save()
        return JsonResponse({
            "correct_option": qn.correct_option,
            "score": qn_attempt.score()
            })

@login_required
def score(request, quiz_id):
    """
    Get the score for a quiz attempt.

    Parameters:
    - request: The HTTP request object.
    - quiz_id: The ID of the quiz.

    Returns:
    - A JSON response containing the score of the quiz attempt.
    """
    quiz = Quiz.objects.get(id=quiz_id)
    quiz_attempt = Quiz_attempt.objects.get(
        user=request.user,
        quiz=quiz
    )
    all_attempts = Quiz_attempt.objects.filter(quiz=quiz).all()
    top_scores = sorted(all_attempts, key=lambda x: x.score(), reverse=True)[:5]
    return JsonResponse({
        "in_leaderboard": quiz_attempt in top_scores,
        "username": quiz_attempt.user.username,
        "score": quiz_attempt.score(),
        "leaderboard": [{
            "username": attempt.user.username,
            "score": attempt.score()
        } for attempt in top_scores]
    })

def login_view(request):
    """
    Logs in a user.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HttpResponseRedirect: If the user is successfully logged in, it redirects to the "quiz:index" page.
    - HttpResponse: If the login is unsuccessful, it renders the "quiz/login.html" template with an error message.
    """
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("quiz:index"))
        else:
            return render(request, "quiz/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "quiz/login.html")


def logout_view(request):
    """
    Logs out the user who made the request.
    
    Parameters:
        request (HttpRequest): The request object representing the current HTTP request.
        
    Returns:
        HttpResponseRedirect: A redirect response to the index page of the quiz app.
    """
    logout(request)
    return HttpResponseRedirect(reverse("quiz:index"))


def register(request):
    """
    Registers a new user.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "quiz/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "quiz/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("quiz:index"))
    else:
        return render(request, "quiz/register.html")
    

@login_required    
def create(request):
    """
    Creates a new quiz.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect response to the "my_quizzes" page if the quiz creation is successful.
        HttpResponse: A rendered HTML response with the "create.html" template and the necessary context variables if the quiz creation is not successful.
    """
    qn_formset = modelformset_factory(Question, form=QuestionForm, extra=0)
    option_formset = modelformset_factory(Option, form=OptionForm, extra=0)

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        qn_forms = qn_formset(request.POST, prefix="question")
        option_forms = option_formset(request.POST, prefix="option")
        print(request.POST)
    else:
        quiz_form = QuizForm()
        qn_forms = qn_formset(queryset=Question.objects.none(), prefix="question")
        option_forms = option_formset(queryset=Option.objects.none(), prefix="option")

    if all([quiz_form.is_valid(), qn_forms.is_valid(), option_forms.is_valid()]):
        save_forms(request, quiz_form, qn_forms, option_forms)
        return HttpResponseRedirect(reverse("quiz:profile", args=[request.user.username]))
    
    else:
        [print(form.errors) for form in [quiz_form, qn_forms, option_forms] if form.errors]
    
    return render(request, "quiz/create.html", {
        "page_title": "New Quiz",
        "quiz_form": quiz_form,
        "qn_forms": qn_forms,
        "option_forms": option_forms
    })


@login_required
def edit(request, quiz_id):
    """
    Edit a quiz.

    Parameters:
        - request: The HTTP request object.
        - quiz_id: The ID of the quiz to be edited.

    Returns:
        - HttpResponseRedirect: If the form is valid and the data is saved successfully, redirects to the 'my_quizzes' page.
        - HttpResponse: If the form is not valid, renders the 'create.html' template with the appropriate forms and data.

    Description:
        This function is responsible for handling the editing of a quiz. 
        It retrieves the quiz, questions, and options associated with the quiz ID and creates formsets for the questions and options. 
        If the request method is 'POST', it validates the form data and saves it. 
        If the form data is valid, the quiz is updated and the user is redirected to the 'my_quizzes' page. 
        If the form data is not valid, the form errors are printed. 
        If the request method is not 'POST', the quiz, question, and option forms are rendered with the appropriate data.

    Note:
        - This function assumes the existence of the following models: Quiz, Question, Option.
        - This function assumes the existence of the following forms: QuizForm, QuestionForm, OptionForm.
        - This function assumes the existence of the 'create.html' template.
    """
    quiz = Quiz.objects.get(id=quiz_id)
    qns = quiz.questions.all().order_by("qn_no")
    options = quiz.options.all().order_by("qn_no", "option_no")
    qn_formset = modelformset_factory(Question, form=QuestionForm, extra=0)
    option_formset = modelformset_factory(Option, form=OptionForm, extra=0)

    if request.method == 'POST':
        print(request.POST)
        quiz_form = QuizForm(request.POST)
        qn_forms = qn_formset(request.POST, prefix="question")
        option_forms = option_formset(request.POST, prefix="option")
        
        if all([quiz_form.is_valid(), qn_forms.is_valid(), option_forms.is_valid()]):
            save_forms(request, quiz_form, qn_forms, option_forms)
            quiz.delete()
            return HttpResponseRedirect(reverse("quiz:profile", args=[request.user.username]))
        else:
            [print(form.errors) for form in [quiz_form, qn_forms, option_forms] if form.errors]

    else:
        quiz_form = QuizForm(instance=quiz)
        qn_forms = qn_formset(queryset=qns, prefix="question")
        option_forms = option_formset(queryset=options, prefix="option")
    
    return render(request, "quiz/create.html", {
        "page_title": "Edit Quiz",
        "quiz_id": quiz_id,
        "quiz_form": quiz_form,
        "qn_forms": qn_forms,
        "option_forms": option_forms
    })

@login_required
def delete(request, quiz_id):
    """
    Delete a quiz.

    Parameters:
        request (HttpRequest): The HTTP request object.
        quiz_id (int): The ID of the quiz to be deleted.

    Returns:
        HttpResponseRedirect: A redirect response to the "my_quizzes" page.
    """
    if request.method == "POST":
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.delete()
        return HttpResponseRedirect(reverse("quiz:profile", args=[request.user.username]))
    else:
        assert False

    
