from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View

from .forms import LoginForm, PasswordRecoveryForm, RegisterForm
from .services import send_mailgun_email


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class RegisterView(View):
    template_name = "accounts/register.html"
    form_class = RegisterForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_mailgun_email(
                subject="Registro exitoso",
                recipient=user.email,
                template_name="emails/welcome.html",
                context={"user": user},
            )
            messages.success(request, "Cuenta creada correctamente.")
            return redirect("home")
        return render(request, self.template_name, {"form": form})


class PasswordRecoveryView(View):
    template_name = "accounts/password_reset.html"
    form_class = PasswordRecoveryForm

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            user = User.objects.filter(email__iexact=email).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(
                    reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
                )
                send_mailgun_email(
                    subject="Recuperacion de cuenta",
                    recipient=user.email,
                    template_name="emails/password_reset.html",
                    context={
                        "user": user,
                        "reset_url": reset_url,
                        "timeout_hours": settings.PASSWORD_RESET_TIMEOUT // 3600,
                    },
                )
            messages.success(
                request,
                "Si el correo existe, enviamos instrucciones para recuperar la cuenta.",
            )
            return HttpResponseRedirect(reverse("password_reset_done"))
        return render(request, self.template_name, {"form": form})

# Create your views here.
