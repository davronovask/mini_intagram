from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from .models import Post, Comment, Like
from users.models import Account, AccountFollower
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from .forms import ProfileForm, PostForm
from django.contrib.auth.decorators import login_required


@login_required
def profile(request, user_id):
    user_profile = get_object_or_404(Account, id=user_id)
    is_following = AccountFollower.objects.filter(follower=request.user, following=user_profile).exists()

    context = {
        'user_profile': user_profile,
        'is_following': is_following,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    user_account = request.user  # Получаем текущего пользователя

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user_account)
        if form.is_valid():
            form.save()  # Сохраняем обновленное описание
            return redirect('profile-url')  # Перенаправляем на страницу профиля
    else:
        form = ProfileForm(instance=user_account)

    return render(request, 'edit_profile.html', {'form': form})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # сохраняем форму, если она валидна
            return redirect('some_success_url')  # редирект на успешную страницу
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})

    class ProfileView(TemplateView):
        template_name = 'profile.html'
class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'user_id' in self.kwargs:
            user_id = self.kwargs['user_id']
            try:
                user_profile = Account.objects.get(id=user_id)
                context['user_profile'] = user_profile
                context['is_following'] = AccountFollower.objects.filter(follower=self.request.user, following=user_profile).exists()
                # Получаем посты этого пользователя
                posts = Post.objects.filter(user=user_profile)
                context['posts'] = posts
            except Account.DoesNotExist:
                context['user_profile'] = None
        else:
            user_profile = self.request.user
            context['user_profile'] = user_profile
            context['is_following'] = False
            posts = Post.objects.filter(user=user_profile)
            context['posts'] = posts

        return context



class CommentView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        content = request.POST.get('content')

        if content:
            Comment.objects.create(
                user=request.user,
                post=post,
                content=content
            )

        return redirect('home-url')

class LikeView(View):
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)

        # Проверяем, есть ли лайк от текущего пользователя для данного поста
        like = Like.objects.filter(user=request.user, post=post).first()

        if like:
            # Если лайк существует, то меняем его статус (лайкнуто/не лайкнуто)
            like.is_liked = not like.is_liked
            like.save()
            liked = like.is_liked
        else:
            # Если лайка нет, создаем новый лайк с is_liked=True
            Like.objects.create(user=request.user, post=post, is_liked=True)
            liked = True

        # Возвращаем информацию о статусе лайка и количестве лайков
        like_count = Like.objects.filter(post=post, is_liked=True).count()
        return JsonResponse({'liked': liked, 'like_count': like_count})


class ReelsView(TemplateView):
    template_name = 'reels.html'

class MessagesView(TemplateView):
    template_name = 'messages.html'




