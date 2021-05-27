from typing import re

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from authapp.models import ShopUser


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print('активация прошла успешно')
        else:
            print(f'Ошибка активации пользователя: {email}')
        return render(request, "authapp/verification.html")
    except Exception as e:
        print(f'Ошибка активации пользователя: {e.args}')
        return HttpResponseRedirect(reverse('main'))


def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    subject = f'активация пользователя {user.username}'
    message = f'для подтверждения перейдите по ссылке: {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def login(request):

    title = "вход"

    next_url = request.GET.get('next', '')

    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))
    from_register = request.session.get('register', None)
    conf_code = request.session.get('conf_code', None)
    email = request.session.get('email', None)
    if from_register:
        del request.session['register']
        del request.session['conf_code']
        del request.session['email']

    content = {
        'title': title,
        'login_form': login_form,
        'next': next_url,
        'from_register': from_register,
        'confirmation': conf_code,
        'pth': f'{settings.DOMAIN_NAME}{request.get_full_path()}{email}{conf_code}',
        'email': email
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):

    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_email(user):
                print('сообщение подтверждения отправлено')
                request.session['register'] = True
                user_name = request.POST['username']
                conf_code, email = [ShopUser.objects.get(username=user_name).activation_key, ShopUser.objects.get(username=user_name).email]
                request.session['conf_code'] = conf_code
                request.session['email'] = email

            else:
                print('ошибка отправки сообщения')
            return HttpResponseRedirect(reverse('auth:login'))

    else:
        register_form = ShopUserRegisterForm()
    content = {
        'title': title,
        'register_form': register_form,
    }
    return render(request, 'authapp/register.html', content)


# class UserEditUpdateView(UpdateView):
#     model = ShopUser
#     template_name = 'authapp/edit.html'
#     form_class = ShopUserEditForm
#
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         context_data['title'] = 'редактирование'
#         return context_data


@login_required
@transaction.atomic()
def edit(request):

    title = 'редактирование'

    if request.method == "POST":
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    ava = request.user.avatar


    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
        'avatar': ava
    }

    return render(request, 'authapp/edit.html', content)