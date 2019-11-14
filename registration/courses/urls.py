from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('profile', views.profile, name="profile"),
    path('courses', views.course_results, name="course_results"),
    path('course/<int:course_id>', views.course, name="course_details"),
    path('course/<int:course_id>/enroll', views.enroll, name="enroll"),
    path('course/<int:course_id>/unenroll', views.unenroll, name="unenroll")
]