from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib import messages
from django.core.mail import send_mail
import random

from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import EmailVerify


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        user = context.get('user', None)
        if not user:
            return 0
        numeric_code = ''.join(random.choices('0123456789', k=6))
        EmailVerify.objects.create(
            user=user,
            email=email,
            key=numeric_code
        )
        # EmailAddress.objects.create(
        #     user=user,
        #     email=email,
        #     primary=True,
        # )
        message = f"Ваш код подтверждения: {numeric_code}"
        send_mail('Код подтверждения', message, 'from@example.com', [email])
        return numeric_code

    def respond_email_verification_sent(self, request, user):
        email = request.POST.get('email', '')
        if not user and EmailAddress.objects.filter(email=email).exists():
            # email уже существует в базе
            messages.error(request, 'Этот адрес электронной почты уже зарегистрирован.')
            return HttpResponseRedirect(reverse('account_signup'))
        request.session['user_id'] = user.id
        request.session['email'] = email
        return HttpResponseRedirect(reverse("confirm_email"))
