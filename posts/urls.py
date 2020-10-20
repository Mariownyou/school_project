from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news, name='news'),
    path('new/', views.new_post, name='new'),
    path('new_category/', views.new_category, name='new_category'),
    path('group/<slug:slug>/', views.group, name='group'),
    path('category/<slug:slug>/', views.category, name='category'),
    path("follow/", views.follow_index, name="follow_index"),
    path("<str:username>/follow/", views.profile_follow, name="profile_follow"),
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path(
        '<str:username>/<int:post_id>/edit/',
        views.post_edit,
        name='post_edit'
    ),
    path("<username>/<int:post_id>/comment", views.add_comment, name="add_comment"),
]
