from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

'''
posts = [
    {
        'author':'Lakshay Chopra',
        'title': 'Blog Post 1',
        'content': 'Hey There',
        'date_posted':'August 5,2019 '
    },
    {
        'author':'Tanisha',
        'title': 'Blog Post 2',
        'content': 'Hello Everyone',
        'date_posted':'August 6,2019 '
    }
]
'''

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'report/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'report/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

class UserPostListView(ListView):
    model = Post
    template_name = 'report/user_posts.html'
    context_object_name = 'posts'
    #ordering = ['-date_posted']
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return false

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return false

def about(request):
    return render(request, 'report/about.html',{'title':'About'})
