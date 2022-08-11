from hashlib import new
import json
from multiprocessing.dummy import JoinableQueue
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Jeopardy, User, Question, Subject, Category
from .forms import NewCategoryForm, NewJeopardyForm, NewQuestionForm
from django.views.generic import ListView



# home page view
def index(request):
    subjects = Subject.objects.all()
    return render(request, "index.html", {
        "subjects":subjects
})


# To show subjects in list view
class SubjectListView(ListView):
    template_name="subject.html"
    context_object_name = 'subjectlist'

    def get_queryset(self):
        content = {
            'subject': self.kwargs['subject'],
            'jeopardys': Jeopardy.objects.filter(subject__choice=self.kwargs['subject'])
        }
        return content


# To show the contents of the requested jeopardy game by jeopardy id
def jeopardy(request, jeopardy_id):
    # retrieve the jeopardy game that matches the id in the url & the categorys that belong to that game
    jeopardy = Jeopardy.objects.get(pk=jeopardy_id)
    categorys = Category.objects.filter(jeopardy=jeopardy.id)

    # create an empty list to store the questions that will be retrieved in next step
    questions = []
    # retrieve the questions for each category within the jeopardy game and store in the list 
    for category in categorys:
        question = Question.objects.filter(category=category.id)
        questions.append(question)

    # Click on Reset button resets all clues to unanswered
    if request.POST.get('Reset') == 'Reset':
        for question in questions:
            for item in question:
                item.answered = False
                item.save()

        return render(request, "jeopardy.html", {
            "jeopardy": jeopardy,
            "categorys": categorys,
            "questions": questions
        })

    return render(request, "jeopardy.html", {
        "jeopardy": jeopardy,
        "categorys": categorys,
        "questions": questions
})


# To retrieve the clue based on the question id
def clues(request):
    data = json.loads(request.body)
    id = int(data.get("id",""))
    clue = Question.objects.get(pk=id)
    return JsonResponse({"message": "Page rendered successfully."}, status=201)


# To show the content of the clue selected from clues function above
def clue(request, question_id):
    try:
        # must use filter instead of get to use .values() function to serialize the queryset to json
        clue = list(Question.objects.filter(pk=question_id).values())
    except Question.DoesNotExist:
        return JsonResponse({"error":"Page not found."}, status=400)

    if request.method == "GET":
        return JsonResponse(clue, safe=False)
    
    else:
        return JsonResponse({"error": "GET request required."}, status=400)


# To mark the answered clue as answered
def answer(request, question_id, choice):
    # answering a clue must be via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    data = json.loads(request.body)
    id = int(data.get("id", ""))
    choice = data.get("choice", "")
    clue = Question.objects.get(pk=id)
    clue.answered = True
    clue.save()
    return JsonResponse({"message": "Clue answered successfully."}, status=201)


# to add new jeopardy game to the database
@login_required
def add(request):
    jeopardys = Jeopardy.objects.all()

    # add new game must be via POST
    if request.method == 'POST':
        jeoform = NewJeopardyForm(request.POST)
        if jeoform.is_valid():
            new_jeopardy = jeoform.save(commit=False)
            # to ensure no two jeopardy games have the same name
            for jeopardy in jeopardys:
                if new_jeopardy.name == jeopardy.name:
                    return render(request, "add.html", {
                        "message": "A jeopardy with the same name already exists, please enter a different name",
                        "jeopardy": NewJeopardyForm(),
                    })
            # assign request user as the owner of the game
            new_jeopardy.owner = request.user
            new_jeopardy.save()
            # redirect to add category page (see addcat function below)
            id = new_jeopardy.id
            return HttpResponseRedirect('/add/%s' % id)
        else:
            return render(request, "add.html", {
                        "message": "Invalid form, please try again",
                        "jeopardy": NewJeopardyForm(),
                    }) 
    # show the form via GET
    return render(request, "add.html", {
        "jeopardy": NewJeopardyForm(),
    })

# to add new category to the newly added jeopardy game
@login_required
def addcat(request, jeopardy_id):
    jeopardy = Jeopardy.objects.get(pk=jeopardy_id)
    categorys = Category.objects.filter(jeopardy=jeopardy.id)

    # redirect to profile page if the request user is not the owner (via url path instead of link path)
    if jeopardy.owner != request.user:
        return HttpResponseRedirect(reverse("profile"))

    # do not show the form if the game already has 5 categorys
    if categorys.count() == 5:
                return render(request, "addcat.html", {
                    "message": "All 5 categorys have been added. Select a category below to add clues for each category",
                    "jeopardy": jeopardy,
                    "categorys": categorys,
                })

    # add new category must be via POST
    if request.method == "POST":
        catform = NewCategoryForm(request.POST)
        if catform.is_valid():
            new_category = catform.save(commit=False)
            # to ensure no duplicate category for that game
            for category in categorys:
                if new_category.category == category.category:
                    return render(request, "addcat.html", {
                        "message": "A category with the same name already exists, please enter a different category name",
                        "category": NewCategoryForm(),
                        "categorys": categorys,
                    })
            new_category.jeopardy = jeopardy
            new_category.save()
            # return the list of categorys again after the new category is added so the latest list is reflected in html
            categorys = Category.objects.filter(jeopardy=jeopardy.id)
            # do not show the form if the game already has 5 categorys
            if categorys.count() == 5:
                return render(request, "addcat.html", {
                    "message": "All 5 categorys have been added. Select a category below to add clues for each category",
                    "jeopardy": jeopardy,
                    "categorys": categorys,
                })
    # show the form via GET
    return render(request, "addcat.html", {
        "jeopardy": jeopardy,
        "category": NewCategoryForm(),
        "categorys": categorys,
    })

        
# to add new questions to the newly added category for the jeopardy game
@login_required
def addques(request, jeopardy_id, category_id):
    jeopardy = Jeopardy.objects.get(pk=jeopardy_id)
    category = Category.objects.get(pk=category_id)
    questions = Question.objects.filter(category=category.id)

    # redirect to profile page if the request user is not the owner (via url path instead of link path)
    if jeopardy.owner != request.user:
        return HttpResponseRedirect(reverse("profile"))

    # do not show the form if the category already has 5 questions
    if questions.count() == 5:
        return render(request, "addques.html", {
            "message": "All 5 clues have been added, return to category page to add more clues to other categories",
            "jeopardy": jeopardy,
            "category": category,
            "questions": questions,
        })

    # add new question must be via POST
    if request.method == "POST":
        quesform = NewQuestionForm(request.POST)
        if quesform.is_valid():
            new_question = quesform.save(commit=False)
            for question in questions:
                # to ensure no duplicate questions for that category
                if new_question.clue == question.clue:
                    return render(request, "addques.html", {
                        "message": "The entered clue already exists, please enter a different clue",
                        "jeopardy": jeopardy,
                        "category": category,
                        "question": NewQuestionForm(),
                        "questions": questions,
                    })
                # to ensure only one question is submitted per cluevalue
                elif new_question.cluevalue == question.cluevalue:
                    return render(request, "addques.html", {
                        "message": "A clue for the selected clue value already exists, please select a different clue value",
                        "jeopardy": jeopardy,
                        "category": category,
                        "question": NewQuestionForm(),
                        "questions": questions,
                    })
            # to ensure at least of the choices matches with the answer
            if new_question.answer != new_question.choiceone and new_question.answer != new_question.choicetwo and new_question.answer != new_question.choicethree:
                return render(request, "addques.html", {
                        "message": "At least one of the choices must be exactly the same as the answer",
                        "jeopardy": jeopardy,
                        "category": category,
                        "question": NewQuestionForm(),
                        "questions": questions,
                    })
            new_question.category = category
            new_question.answered = False
            new_question.save()
            # return the list of questions again after the new question is added so the latest list is reflected in html
            questions = Question.objects.filter(category=category.id)
            # do not show the form if the category already has 5 questions
            if questions.count() == 5:
                return render(request, "addques.html", {
                    "message": "All 5 clues have been added, return to category page to add more clues to other categories",
                    "jeopardy": jeopardy,
                    "category": category,
                    "questions": questions,
                })
    # show the form via GET
    return render(request, "addques.html", {
        "jeopardy": jeopardy,
        "category": category,
        "question": NewQuestionForm(),
        "questions": questions,
    })

# to show the user profile page where the user contributed games can be accessed
@login_required
def profile(request):
    user = User.objects.get(username=request.user.username)
    jeopardys = Jeopardy.objects.filter(owner = user)
    return render(request, "profile.html",{
        "user": user,
        "jeopardys": jeopardys
    })
    
# to log in user
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

# to log out user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# to resgiter user
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Ensure all fields are completed
        if not username or not email or not password or not confirmation:
            return render(request, "register.html", {
                "message": "Please complete all required fields."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

