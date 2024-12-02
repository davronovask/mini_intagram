from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from users.views import UserRegistrationView, LoginPageView, UserMakeLoginView, UserMakeRegistrationView
from posts.views import ProfileView, ReelsView, MessagesView, LikeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', UserRegistrationView.as_view(), name='registration-url'),
    path('login/', LoginPageView.as_view(), name='login-url'),  # Добавляем имя для пути логина
    path('make-login/', UserMakeLoginView.as_view(), name='make-login-url'),
    path('make-registration/', UserMakeRegistrationView.as_view(), name='make-registration-url'),

    path('profile/', ProfileView.as_view(), name='profile-url'),
    path('reels/', ReelsView.as_view(), name='reels-url'),
    path('like/<int:post_id>/', LikeView.as_view(), name='like-url'),
    path('messages/', MessagesView.as_view(), name='messages-url'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)