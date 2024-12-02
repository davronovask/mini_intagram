from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .models import Post, Comment, Like
from users.models import Account, AccountFollower
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        current_user = self.request.user

        followers_count = current_user.my_followers.all().count()
        following_count = current_user.my_following.all().count()
        posts_count = current_user.post.all().count()

        context = {
            'followers_count': followers_count,
            'following_count': following_count,
            'posts_count': posts_count,
        }
        return context



class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        current_user = self.request.user

        # Получаем всех пользователей, на которых подписан текущий пользователь
        following_users = AccountFollower.objects.filter(follower=current_user).values_list('following', flat=True)

        # Получаем посты только от тех пользователей, на которых подписан текущий пользователь
        posts = Post.objects.filter(user__in=following_users)

        context = {
            'posts': posts,
        }
        return render(request, self.template_name, context)


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


