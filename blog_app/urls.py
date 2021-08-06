from django.urls import path
from .views import home, about, register, profile, PostCreateview, PostListView, PostDetailView, PostUpdateView, \
    PostDeleteView,UserPostListView

urlpatterns = [
    # path('',home,name='blog-home'),
    path('', PostListView.as_view(), name='blog-home'),
    path('post/create/', PostCreateview.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

    path('about/', about, name='blog-about'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),

]
