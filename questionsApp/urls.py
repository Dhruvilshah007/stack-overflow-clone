from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),


    path('userSignup/', views.userSignup, name='userSignup'),
    path('userLogin/', views.userLogin, name='userLogin'),
    path('userLogout/', views.userLogout, name='userLogout'),


    path('viewQuestion/', views.viewQuestion, name='viewQuestion'),
    path('createQuestion/', views.createQuestion, name='createQuestion'),

    path('viewQuestion/detailviewQuestion/<int:qid>', views.detailviewQuestion,
         name='detailviewQuestion'),

    path('profile/', views.profile,
         name='profile'),
    path('editQuestion/<int:qid>', views.editQuestion,
         name='editQuestion'),
    path('deleteQuestion/<int:qid>', views.deleteQuestion,
         name='deleteQuestion'),

    path('forgotPassword/', views.ResetPassword,
         name='forgotPassword'),
    path('setNewPassword/<uidb64>/<token>', views.setNewPassword,
         name='setNewPassword'),


]
