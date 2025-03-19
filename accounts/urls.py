from django.urls import path
from .views import register, user_login, dashboard_view, user_logout

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("logout/", user_logout, name="logout"),
]
