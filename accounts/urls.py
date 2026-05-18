from django.contrib.auth.views import LogoutView, PasswordResetCompleteView, PasswordResetConfirmView
from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .views import CustomLoginView, PasswordRecoveryView, RegisterView


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("password-reset/", PasswordRecoveryView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        TemplateView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
