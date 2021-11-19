from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Question
from django.http import HttpResponse


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

# def createQuestion(request):
# def deleteQuestion(request):
# def editQuestion(request):
