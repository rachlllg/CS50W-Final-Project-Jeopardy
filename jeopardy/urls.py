from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("add/<int:jeopardy_id>",views.addcat, name="addcat"),
    path("add/<int:jeopardy_id>/<int:category_id>",views.addques, name="addques"),
    path("profile", views.profile, name="profile"),
    path("<subject>", views.SubjectListView.as_view(), name="subject"),
    path("jeopardy/<int:jeopardy_id>", views.jeopardy, name="jeopardy"),


    #API Routes:
    path("clue", views.clues, name='clues'),
    path("clue/<int:question_id>", views.clue, name='clue'),
    path("clue/<int:question_id>/<choice>", views.answer, name="answer"),

]