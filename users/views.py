from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import AvatarForm
from users.models import Account

from .models import AccountFollower
from posts.models import Post


class UserRegistrationView(TemplateView):
    template_name = 'sign_up.html'


class LoginPageView(TemplateView):
    template_name = 'login.html'


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        following_users = AccountFollower.objects.filter(follower=current_user)
        following_user_ids = [f.following.id for f in following_users]

        # Получаем все посты текущего пользователя и тех, на кого он подписан
        posts = Post.objects.filter(user__in=following_user_ids + [current_user.id])
        context = {'posts': posts}
        return context


class UserMakeLoginView(View):
    """Логическая Вююшка для Логина """
    template_name = 'home.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username_address')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'home.html')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})


class UserMakeRegistrationView(View):
    """Логическая Вююшка для регистрации"""
    template_name = 'home.html'

    def post(self, request, *args, **kwargs):
        data = request.POST

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username_address')
        password = data.get('password')

        if get_user_model().objects.filter(username=username).exists():
            return render(
                request, 'sign_up.html', {'error': 'Пользователь с таким именем уже существует.'}
            )

        if password:
            user = Account.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            return render(request, 'home.html')
        else:
            return render(request, 'sign_up.html', {'error': 'Что-то пошло не так.'})


