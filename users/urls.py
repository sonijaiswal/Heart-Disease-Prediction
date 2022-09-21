from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("", views.userAccount, name="account"),
    path("edit-details/", views.ediDetail, name="edit-details"),
    path("check-heart/", views.checkHeart, name="check-heart"),
    path("edit-account/", views.editAccount, name="edit-account"),
    path("inbox/", views.inbox, name="inbox"),
    path("message/<str:pk>/", views.viewMessage, name="message"),
    path("create-message/<str:pk>/", views.createMessage, name="create-message"),
]
