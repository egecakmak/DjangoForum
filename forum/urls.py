from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('users/<int:user_id>', views.users, name='users'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('startThread/', views.start_thread, name='start_thread'),
    path('threads/', views.threads, name='threads'),
    path('threads/<int:thread_id>', views.thread, name='thread'),
    path('threads/<int:thread_id>/deletePost/<int:post_id>', views.delete_post, name='delete_post'),
    path('threads/<int:thread_id>/editPost/<int:post_id>', views.edit_post, name='edit_post'),
    # path('messages/', views.messages, name='messages'),
    # path('messages/<int:message_container_id>/', views.conversations, name='conversations'),
]