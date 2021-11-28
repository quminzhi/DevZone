from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('base.urls')),
    path('', include('users.urls')),

    # 1. User submits email for reset
    # 2. Email sent message
    # 3. Email with link and reset instructions
    # 4. Password successfully reset message
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='reset/reset-password.html'),
         name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset/reset-password-sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset/reset.html'),
         name="password_reset_confirm"),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset/reset-complete.html'),
         name="password_reset_complete")

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# static files can be accessed in release mode
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
