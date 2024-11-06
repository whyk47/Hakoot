from django.core.paginator import Paginator

def get_page(request, quizzes):
    """
    Retrieves a specific page of quizzes from the given list of quizzes.

    Parameters:
        request (HttpRequest): The HTTP request object.
        quizzes (list): A list of quizzes.

    Returns:
        Page: The specific page of quizzes.
    """
    paginator = Paginator(quizzes, 10)
    page_no = request.GET.get("page")
    page = paginator.get_page(page_no)
    return page


def save_forms(request, quiz_form, qn_forms, option_forms):
    """
    Save the forms for creating a quiz.

    Args:
        request: The HTTP request object.
        quiz_form: The form for creating a quiz.
        qn_forms: The forms for creating quiz questions.
        option_forms: The forms for creating question options.

    Returns:
        None
    """
    quiz = quiz_form.save(commit=False)
    quiz.creator = request.user
    quiz.save()

    for i, qf in enumerate(qn_forms):
        qn = qf.save(commit=False)
        qn.quiz = quiz
        qn.qn_no = i
        qn.save()

        for j in range(4):
            option_form = option_forms[i * 4 + j]
            option = option_form.save(commit=False)
            option.quiz = quiz
            option.question = qn
            option.qn_no = i
            option.option_no = j
            option.save()
            