import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Answer, Question
from django.http import HttpResponse
from .forms import Question_Form
from django.urls import reverse


# Basic pages Home and About
def home(request):
    return render(request, 'BasicpagesFolder/home.html')


def about(request):
    return render(request, 'BasicpagesFolder/about.html')


# ----------------------------------------------------------------------------------------------------------------------------------------
# Authentication stuff
# ----------------------------------------------------------------------------------------------------------------------------------------


def userSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['emailid']
        password = request.POST['pwd']

        # checks for errorneous input
        # username should be <10
        # username shouldbe alphanumeric
        # same username

        if User.objects.filter(email=email).exists():
            messages.error(
                request, "Please write correct email ID,user with this emailID already exists ")
            return redirect('/userSignup')

        if User.objects.filter(username=username).exists():
            messages.error(
                request, "Please choose another username this user with this username already exists ")
            return redirect('/userSignup')

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

    return render(request, 'UserpagesFolder/userSignup.html')


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

    return render(request, 'UserpagesFolder/userLogin.html')


def userLogout(request):
    logout(request)
    messages.success(request, "Logged Out Succesfully")
    return redirect('/')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('/userLogin')
    all_user_questions = Question.objects.filter(question_author=request.user)
    context = {
        'all_user_data': all_user_questions
    }
    return render(request, 'UserpagesFolder/profile.html', context)

# ----------------------------------------------------------------------------------------------------------------------------------------
# Questions-CRUD
# ----------------------------------------------------------------------------------------------------------------------------------------


def viewQuestion(request):
    viewQuestions = Question.objects.all()
    context = {'viewQuestions': viewQuestions}
    return render(request, 'QuestionsFolder/viewQuestion.html', context)


def createQuestion(request):

    if not request.user.is_authenticated:
        return redirect('/userLogin')

    if request.method == 'POST':
        questionform = Question_Form(request.POST)
        if questionform.is_valid():
            formVar = questionform.save(commit=False)
            formVar.question_author = request.user
            formVar.save()
            questionform.save_m2m()
            messages.success(request, "Question Posted Succesfully")
            return redirect('viewQuestion')
        else:
            print("something wrong")
    formqs = Question_Form()
    d = {
        'forms': formqs
    }
    return render(request, 'QuestionsFolder/createQuestion.html', d)


def deleteQuestion(request, qid):
    if not request.user.is_authenticated:
        return redirect('/userLogin')
    obj = get_object_or_404(Question, question_id=qid)
    all_user_data = Question.objects.filter(
        question_id=qid, question_author=request.user)
    if not all_user_data:
        return HttpResponse("you have no access")

    all_user_data.delete()
    messages.success(request, "Question Deleted Succesfully")
    return redirect('profile')


def editQuestion(request, qid):
    if not request.user.is_authenticated:
        return redirect('/userLogin')

    obj = get_object_or_404(Question, question_id=qid)
    if request.method == 'GET':

        form = Question_Form(request.POST or None, instance=obj)

        context = {
            'form': form
        }
        return render(request, "QuestionsFolder/editQuestion.html", context)

    if request.method == 'POST':
        all_user_data = Question.objects.filter(
            question_id=qid, question_author=request.user)
        if not all_user_data:
            return HttpResponse("you have no access")

        form = Question_Form(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Question Updated Succesfully")

        return redirect('profile')


def detailviewQuestion(request, qid):
    soln = Question.objects.get(question_id=qid)

    question_data = Question.objects.filter(question_id=qid)
    answser = Answer.objects.filter(parent_question_id=qid)
    if request.method == 'GET':
        context = {
            'soln': question_data,
            'ans': answser,
        }
        return render(request, 'QuestionsFolder/detailviewQuestion.html', context)

    if request.method == 'POST':
        ans_body = request.POST['answer_body']

        Answer.objects.create(
            answer_body=ans_body, parent_question=soln, user_answering=request.user)
        return redirect(reverse('detailviewQuestion', kwargs={'qid': qid}))


class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


def ResetPassword(request):
    context = {
        'has_error': False
    }

    if request.method == 'POST':
        email = request.POST['email']

        user_email_check = User.objects.filter(email=email)

        if email == '':
            messages.add_message(request, messages.ERROR, 'Email is required')
            context['has_error']: True

        if user_email_check:
            pass
        else:
            messages.add_message(request, messages.ERROR,
                                 'Email is not registered')
            context['has_error']: True

        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_subject = 'Password Reset Request'
            message = render_to_string('UserpagesFolder/ResetPasswordEmailForm.html',
                                       {
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                                           'token': PasswordResetTokenGenerator().make_token(user[0]),

                                       }
                                       )
            message_content = strip_tags(message)

            email_message = EmailMultiAlternatives(
                email_subject,
                message_content,
                settings.EMAIL_HOST_USER,
                [email],
            )

            email_message.attach_alternative(message, "text/html")

            EmailThread(email_message).start()

            messages.success(
                request, 'We have sent you email with instruction on how to reset password')
            return render(request, 'UserpagesFolder/forgotPassword.html')

    return render(request, 'UserpagesFolder/forgotPassword.html')


def setNewPassword(request, uidb64, token):
    if request.method == 'GET':
        context = {
            'uidb64': uidb64,
            'token': token
        }
        return render(request, 'UserpagesFolder/setNewPassword.html', context)

    if request.method == 'POST':
        context = {
            'uidb64': uidb64,
            'token': token,
            'has_error': False
        }

        password = request.POST['password']
        password1 = request.POST['password1']

        if password == '':
            messages.add_message(request, messages.ERROR,
                                 'Password is required')
            context['has_error']: True

        if password1 == '':
            messages.add_message(request, messages.ERROR,
                                 'Confirm Password is required')
            context['has_error']: True

        if password != password1:
            messages.add_message(request, messages.ERROR, 'Password Not Match')
            context['has_error'] = True

        if len(password) < 7:
            messages.add_message(request, messages.ERROR,
                                 'password shod be Atleast 7 character or more')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'UserpagesFolder/setNewPassword.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(
                request, 'password reset success, you can login with new password')
            return redirect('userLogin')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Something went wrong')
            return render(request, 'userall/set-new-password.html', context)

    return render(request, 'UserpagesFolder/setNewPassword.html')
