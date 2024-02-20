from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Post

# класс для главной страницы
class BlogListView(ListView):
    model = Post
    ordering = ['-pub_date']
    template_name = "home.html"

# класс для страницы с отдельным постом по сслеке которого я могу перейти
class BlogDetailView(DetailView):
    model = Post
    ordering = ['-pub_date']
    template_name = 'post_detail.html'

# класс для создния нового поста
class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['title', 'author', 'body']

class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']

class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')