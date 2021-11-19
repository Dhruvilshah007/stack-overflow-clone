from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Answer, Question
from django.http import HttpResponse
import datetime
from .forms import Question_Form


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

# Authentication stuff


def userSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['emailid']
        password = request.POST['pwd']

        # checks for errorneous input
        # username should be <10
        # username shouldbe alphanumeric

        if len(username) > 10:
            messages.error(request, "username must be less than 10 characters")
            return redirect('/userSignup')
        if not username.isalnum():
            messages.error(
                request, "username should only contain letters and numbers")
            return redirect('/userSignup')

        # Create the user
        myuser = User.objects.create_user(username, email, password)
        myuser.user_name = username
        myuser.user_email = email
        myuser.save()
        messages.success(
            request, "Your Stackoverflow account has been created succesfully Now enter your credentials into the login form")
        return redirect('/userLogin')

    return render(request, 'userSignup.html')


def userLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['username']
        loginpassword = request.POST['password']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Succesfully Logged In")
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials Please try again")
            return redirect('/userLogin')

        return HttpResponse('404 - Not Found')

    return render(request, 'userLogin.html')


def userLogout(request):
    logout(request)
    messages.success(request, "Logged Out Succesfully")
    return redirect('/')


# Question
def viewQuestion(request):
    viewQuestions = Question.objects.all()
    d = {'viewQuestions': viewQuestions}
    return render(request, 'QuestionsFolder/viewQuestion.html', d)


def createQuestion(request):
    # if not request.user.is_authenticated:
    #     return redirect('/userLogin')
    # error = ""
    # if request.method == 'POST':
    #     questionTitle = request.POST['title']
    #     questionBody = request.POST['body']
    #     questionStatus = request.POST['status']
    #     questionTags = request.POST['tags']
    #     questionUsername = User.objects.filter(
    #         Username=request.user.username).first()
    #     try:
    #         Question.objects.create(question_author=questionUsername, question_title=questionTitle,
    #                                 question_body=questionBody, created_at=datetime.datetime.now(), question_status=questionStatus,
    #                                 question_tags=questionTags)
    #         error = "no"
    #     except:
    #         error = "yes"
    # d = {'error': error}

    if not request.user.is_authenticated:
        return redirect('/userLogin')

    if request.method == 'POST':
        fq = Question_Form(request.POST)
        if fq.is_valid():
            new_emp = fq.save(commit=False)
            new_emp.question_author = request.user
            new_emp.save()
            fq.save_m2m()
        else:
            print("something wrong")
    fo = Question_Form()
    d = {
        'forms': fo
    }
    return render(request, 'QuestionsFolder/createQuestion.html', d)


def deleteQuestion(request, qid):
    obj = get_object_or_404(Question, question_id=qid)
    all_user_data = Question.objects.filter(
        question_id=qid, question_author=request.user)
    if not all_user_data:
        return HttpResponse("you have no access")

    obj.delete()
    return render(request, 'profile.html')


def editQuestion(request, qid):
    obj = get_object_or_404(Question, question_id=qid)
    all_user_data = Question.objects.filter(
        question_id=qid, question_author=request.user)
    if not all_user_data:
        return HttpResponse("you have no access")

    form = Question_Form(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, "QuestionsFolder/editQuestion.html", context)


# def profile(request):
#     all_user_questions = Question.objects.filter(question_author=request.user)
#     context = {
#         'all_user_data': all_user_questions
#     }
#     return render(request, 'profile.html', context)


def detailviewQuestion(request, qid):
    soln = Question.objects.get(question_id=qid)
    # print(soln)
    # answser = Answer.objects.filter(parent_question_id=qid)
    if request.method == 'GET':
        aw = Answer.objects.select_related(
            'parent_question').filter(parent_question_id=qid)

        d = {
            # 'soln': soln,
            # 'ans': answser,
            'aw': aw
        }
        return render(request, 'QuestionsFolder/detailviewQuestion.html', d)

    if request.method == 'POST':
        aa = request.POST['answer_body']

        Answer.objects.create(
            answer_body=aa, parent_question=soln, user_answering=request.user)
        return render(request, 'QuestionsFolder/detailviewQuestion.html')
