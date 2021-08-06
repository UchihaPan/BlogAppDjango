from django.shortcuts import render, redirect,get_object_or_404
from .forms import Userregister, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from .models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = Userregister(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration sucessfull')
            return redirect('blog-home')

    else:
        form = Userregister()
        return render(request, 'blog_app/register.html', {'form': form})


def home(request):
    post = Post.objects.all()
    return render(request, 'blog_app/index.html', {'post': post})


class PostListView(ListView):
    model = Post
    template_name = 'blog_app/index.html'
    context_object_name = 'post'
    ordering = ['-date_posted']

class UserPostListView(ListView):
    model = Post
    template_name = 'blog_app/user_post_list.html'
    context_object_name = 'post'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostCreateview(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user != post.author:
            return False
        return True


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog_app/post_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user != post.author:
            return False
        return True


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/post_detail.html'
    context_object_name = 'post'


def about(request):
    return render(request, 'blog_app/about.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'update sucessfull')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(request.FILES, instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog_app/profile.html', context)
