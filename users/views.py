from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import AvatarForm
from users.models import Account
from django.contrib import messages
from .models import AccountFollower
from posts.models import Post

from posts.models import Like, Comment




def search_users(request):
    query = request.GET.get('q', '')  # Получаем запрос из URL
    users = Account.objects.filter(username__icontains=query)  # Ищем пользователей по имени

    return render(request, 'search_results.html', {
        'query': query,
        'users': users
    })

    return render(request, 'search_results.html', {'users': users, 'query': query})
@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(Account, id=user_id)

    # Проверяем, подписан ли уже текущий пользователь
    if not AccountFollower.objects.filter(follower=request.user, following=user_to_follow).exists():
        AccountFollower.objects.create(follower=request.user, following=user_to_follow)
        messages.success(request, "Вы подписались на пользователя.")
    else:
        messages.info(request, "Вы уже подписаны на этого пользователя.")

    return redirect('profile-url', user_id=user_to_follow.id)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(Account, id=user_id)

    # Проверяем, подписан ли текущий пользователь
    if AccountFollower.objects.filter(follower=request.user, following=user_to_unfollow).exists():
        # Удаляем подписку
        AccountFollower.objects.filter(follower=request.user, following=user_to_unfollow).delete()
        messages.success(request, "Вы отписались от пользователя.")
    else:
        messages.info(request, "Вы не подписаны на этого пользователя.")

    return redirect('profile-url', user_id=user_to_unfollow.id)

class UserRegistrationView(TemplateView):
    template_name = 'sign_up.html'

class LoginPageView(TemplateView):
    template_name = 'login.html'


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        current_user = self.request.user

        # Находим всех пользователей, на которых подписан текущий пользователь
        following_users = AccountFollower.objects.filter(follower=current_user)
        following_user_ids = [f.following.id for f in following_users]

        # Получаем все посты текущего пользователя и тех, на кого он подписан
        posts = Post.objects.filter(user__in=following_user_ids + [current_user.id])

        # Добавляем информацию о лайках для каждого поста
        posts_with_likes = []
        for post in posts:
            post.is_liked = Like.objects.filter(user=current_user, post=post).exists()
            post.likes_count = post.likes.count()  # Количество лайков
            # Получаем все комментарии с использованием обратной связи
            post.comments_list = post.comments.all()  # Получаем все комментарии
            posts_with_likes.append(post)

        # Получаем всех пользователей, за исключением текущего
        all_users = Account.objects.exclude(id=current_user.id)

        # Получаем всех пользователей, на которых подписан текущий пользователь
        following_user_ids = [f.following.id for f in following_users]

        # Отбираем пользователей, на которых текущий пользователь не подписан
        suggested_users = all_users.exclude(id__in=following_user_ids)

        context = {
            'posts': posts_with_likes,
            'suggested_users': suggested_users,  # Добавляем рекомендованных пользователей
        }

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
    """Логика для регистрации пользователя"""

    def post(self, request, *args, **kwargs):
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username_address')
        password = data.get('password')

        if get_user_model().objects.filter(username=username).exists():
            return render(request, 'sign_up.html', {'error': 'Пользователь с таким именем уже существует.'})

        if password:
            user = Account.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            # Перенаправляем на страницу для загрузки аватара
            return redirect('upload_avatar', user_id=user.id)
        else:
            return render(request, 'sign_up.html', {'error': 'Что-то пошло не так.'})

class UploadAvatarView(View):
    """Страница для загрузки аватара"""

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = Account.objects.get(id=user_id)  # Получаем пользователя по user_id
        except Account.DoesNotExist:
            return redirect('home-url')  # Если пользователя нет, перенаправляем на главную

        form = AvatarForm(instance=user)  # Создаем форму с существующим пользователем
        return render(request, 'upload_avatar.html', {'form': form})

    def post(self, request, user_id, *args, **kwargs):
        try:
            user = Account.objects.get(id=user_id)  # Получаем пользователя по user_id
        except Account.DoesNotExist:
            return render(request, 'upload_avatar.html', {'error': 'Пользователь не найден.'})

        form = AvatarForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('profile-url', user_id=user.id)  # Перенаправление на профиль пользователя

        return render(request, 'upload_avatar.html', {'form': form, 'error': 'Ошибка при загрузке аватара'})