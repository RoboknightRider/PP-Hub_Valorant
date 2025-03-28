from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('file/<int:pk>/', views.uploaded_file_detail, name='uploaded_file_detail'),
    path('files', views.files, name='files'),
    path('delete_file/<int:pk>/', views.delete_file, name='delete_file'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
    path("settings/", views.settings_view, name="settings"),
    path('api/get_messages/', views.get_messages, name='get_messages'),
    path('api/save_message/', views.save_message, name='save_message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)