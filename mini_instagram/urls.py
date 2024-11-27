from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from users.views import UserRegistrationView, LoginPageView, UserMakeLoginView, UserMakeRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', UserRegistrationView.as_view(), name='registration-url'),
    path('login/', LoginPageView.as_view(), name='login-url'),  # Добавляем имя для пути логина
    path('make-login/', UserMakeLoginView.as_view(), name='make-login-url'),
    path('make-registration/', UserMakeRegistrationView.as_view(), name='make-registration-url'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)