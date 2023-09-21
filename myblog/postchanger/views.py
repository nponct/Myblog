from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q

from .utils import *
from .models import Category, ArtPost, Comment
from .forms import AddPostForm, CommentForm, RegisterUserForm, LoginUserForm, SearchForm


class PostView(DataMixin,ListView):
    model = ArtPost
    template_name = 'postchanger/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def=self.get_user_context(title = 'Главная страница')
        return dict(list(context.items())+list(c_def.items()))


def about(request):
    return render(request, 'postchanger/about.html', {'menu': menu, 'title': 'О нас'})


def search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        q = search_form.cleaned_data['q']
        artposts = ArtPost.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q) |
            Q(time_create__icontains=q)
            )
        context = {'artposts': artposts, 'q': q}
        return render(
        request,
        'postchanger/search.html',
        context
        )


class AddPost(DataMixin,CreateView):
    form_class = AddPostForm
    template_name = 'postchanger/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление страницы')
        return dict(list(context.items()) + list(c_def.items()))



def contact(request):
    return HttpResponse("Обратная связь")


#def login(request):
    #return HttpResponse("Авторизация")

def pageNotFound(request,exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class ShowPost(DataMixin,DetailView):
    model = ArtPost
    template_name = 'postchanger/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        connected_comments = Comment.objects.filter(commentpost=self.get_object())
        number_of_comments = connected_comments.count()
        c_def = self.get_user_context(title=context['post'],comments=connected_comments,
                                      no_of_comments=number_of_comments,comment_form=CommentForm())
        return dict(list(context.items()) + list(c_def.items()))


    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            print('-------------------------------------------------------------------------------Reached here')
            comment_form = CommentForm(self.request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data['content']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent = None

            new_comment = Comment(content=content, author=self.request.user, commentpost=self.get_object(),
                                  parent=parent)
            new_comment.save()
            return redirect(self.request.path_info)


class CategoryView(DataMixin,ListView):
    model = ArtPost
    template_name = 'postchanger/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return ArtPost.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title= 'Категория-' + str(context['posts'][0].cat),
                                      cat_selected= context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin,CreateView):
    form_class = RegisterUserForm
    template_name = 'postchanger/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        return redirect('home')

class LoginUser(DataMixin,LoginView):
    form_class = LoginUserForm
    template_name = 'postchanger/login.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect ('login')







