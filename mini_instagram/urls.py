# mini_instagram/urls.py

from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from users.views import follow_user, unfollow_user, search_users
from posts import views
from users.views import UserRegistrationView, LoginPageView, UserMakeLoginView, UserMakeRegistrationView, HomeView, \
    UploadAvatarView
from posts.views import ProfileView, ReelsView, MessagesView, LikeView, AddCommentView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', UserRegistrationView.as_view(), name='registration-url'),
    path('login/', LoginPageView.as_view(), name='login-url'),
    path('make-login/', UserMakeLoginView.as_view(), name='make-login-url'),
    path('home/', HomeView.as_view(), name='home-url'),
    path('make-registration/', UserMakeRegistrationView.as_view(), name='make-registration-url'),
    path('profile/', ProfileView.as_view(), name='profile-url'),  # Эта строка может быть удалена или обновлена
    path('reels/', ReelsView.as_view(), name='reels-url'),
    path('messages/', MessagesView.as_view(), name='messages-url'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # Подписка и отписка
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),

    # Загрузка аватара
    path('upload-avatar/<int:user_id>/', UploadAvatarView.as_view(), name='upload_avatar'),

    # Лайк на посте
    path('like/<int:post_id>/', LikeView.as_view(), name='like-url'),


    # Поиск пользователей
    path('search/', search_users, name='search-users-url'),  # Поиск пользователей
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile-url'),  # Это путь для конкретного профиля

    path('create/', views.create_post, name='create-post'),

    path('add-comment/<int:pk>/', AddCommentView.as_view(), name='add-comment-url'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
