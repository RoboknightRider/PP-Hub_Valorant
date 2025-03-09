from django.contrib import admin
from django.urls import path, include
from accounts.views import user_login

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", user_login, name="home"),
    path("accounts/", include("accounts.urls")),
]
