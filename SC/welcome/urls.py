from django.urls import path
from .views import *


urlpatterns = [
    path('', welcomeView, name='welcome'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout_request, name='logout'),
    path('home/', home, name='home'),
    path('password/', change_password, name='change_password'),
    path('delete/<int:pk>', deleteAccount, name="deleteAccount"),
    path('adeletes/<str:name>', adeletes, name="adeletes"),
    path('profile/<int:pk>', profile, name='profile'),
    path('profile/project/<int:pk>/delete/', deleteProject, name="deleteProject"),
    path('profile/project/<int:pk>/edit/', editProject, name="editProject"),
    path('profile/post/<int:pk>/delete/', deletePost, name="deletePost"),
    path('profile/post/<int:pk>/edit/', editPost, name="editPost"),
    path('profile/<int:pk>/project/add', addProject, name="addProject"),
    path('profile/<int:pk>/post/add', addPost, name="addPost"),
    path('profile/<int:pk>/edit', editAccount, name="editAccount"),
    path('generate_token/', generate_token, name="generate_token"),
    path('reset_password/', reset_password, name="reset_password"),
]

