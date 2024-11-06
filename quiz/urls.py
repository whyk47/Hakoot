from django.urls import path
from . import views

app_name = "quiz"
urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.index, name="profile"),
    path("view/<int:quiz_id>", views.view, name="view"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("edit/<int:quiz_id>", views.edit, name="edit"),
    path("delete/<int:quiz_id>", views.delete, name="delete"),
    path("play/<int:quiz_id>", views.play, name="play"),
    path("play/score/<int:quiz_id>", views.score, name="score"),
]