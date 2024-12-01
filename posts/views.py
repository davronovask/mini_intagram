from django.shortcuts import render
from django.views.generic import TemplateView, View
from .models import Post
from users.models import Account, AccountFollower
class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        current_user = self.request.user

        followers_count = current_user.my_followers.all().count()
        following_count = current_user.my_following.all().count()

        posts_count = current_user.posts.all().count()

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



class ReelsView(TemplateView):
    template_name = 'reels.html'


