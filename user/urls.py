from django.urls import path

from .views      import DeleteAccountView, SignUpView, SignInView

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/<int:user_id>',DeleteAccountView.as_view())
]
