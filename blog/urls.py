from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/create/', views.blog_create, name='blog_create'),
    path('blogs/<int:blog_id>/edit/', views.blog_edit, name='blog_edit'),
    path('blogs/<int:blog_id>/delete/', views.blog_delete, name='blog_delete'),

    # Auth URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
