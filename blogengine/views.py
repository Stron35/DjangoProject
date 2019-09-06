from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin
from django.views.generic.base import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Gallery, Comment
from .forms import *

# Create your views here.
def post_list(request):
    posts = Post.objects.all().order_by('-create_at')
    return render(request, 'blogengine/posts_list.html', {'posts': posts})

# def post_detail(request, slug):
#     post = get_object_or_404(Post, slug__iexact = slug)
#     return render(request, 'blogengine/post_detail.html', {'post': post})

class PostDetailView(DetailView):
    model = Post
    template_name = 'blogengine/post_detail.html'
    # form_class = CommentForm

    # def get_success_url(self):
    #     return reverse('post_detail', kwargs={'slug':self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['commentform'] = CommentForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug__iexact = kwargs['slug'])
        form = CommentForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = post
            obj.author = self.request.user
            obj.save()
            return redirect('post_detail', post.slug)


    # def form_valid(self, form):
    #     form.save()
    #     return super(PostDetailView, self).form_valid(form)


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text']

    def form_valid(self,form):
        new_post = form.save(commit = False)
        new_post.author = self.request.user
        new_post.save()
        for item in self.request.FILES.getlist('gallery'):
            Gallery.objects.create(image = item, thumbnail = item, post = new_post)
        return super().form_valid(form)

    def get(self, request):
        form = PostForm()
        title = 'Post create'
        return render(request, 'blogengine/post_create.html',{'form':form, 'title':title})


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text']

    def get(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, slug__iexact = kwargs['slug'])
        self.form = PostForm(instance = self.post)
        title = 'Post edit'
        return render(request, 'blogengine/post_create.html', {'form': self.form, 'post':self.post, 'title':title})

    def form_valid(self, form):
        edit_post = form.save(commit=False)
        edit_post.author = self.request.user
        edit_post.save()
        for item in self.request.FILES.getlist('gallery'):
            Gallery.objects.create(image = item, thumbnail = item, post = edit_post)
        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post

    def get(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, slug__iexact = kwargs['slug'])
        self.form = PostForm(instance = self.post)
        title = 'Post edit'
        return render(request, 'blogengine/post_confirm_delete.html', {'form': self.form, 'post':self.post, 'title':title})

    def post(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, slug__iexact = kwargs['slug'])
        self.post.delete()
        return redirect(reverse('posts_list'))


# class CommentCreate(LoginRequiredMixin, CreateView):
#     model = Comment
#     fields = ('text',)

#     # success_url = '/'
#     # template_name = 'blogengine/post_detail.html'

#     # def get_context_data(self, **kwargs):
#     #     context = super(CommentCreate, self).get_context_data(**kwargs)
#     #     context['comment']= CommentForm()
#     #     return context

#     def form_valid(self, form):
#         self.post = get_object_or_404(Post, slug__iexact = kwargs['slug'])
#         comment = form.save(commit = False)
#         print(form)
#         comment.post = self.post
#         comment.author = self.request.user
#         comment.save()
#         return redirect('post_detail', slug=self.post.slug)



class RegistrationFormView(FormView):
    form_class = RegisterForm
    success_url = '/accounts/login/'
    template_name = 'blogengine/registration.html'

    def form_valid(self, form):
        print(form)
        form.save()
        return super(RegistrationFormView, self).form_valid(form)

    def form_invalid(self, form):
        print(form)
        return super(RegistrationFormView, self).form_invalid(form)


class LoginFormView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'blogengine/login.html'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse('posts_list'))


class ProfileView(DetailView):
    model = User
    template_name = 'blogengine/profile.html'
    slug_field = 'username'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('userImage','bio')
    slug_field = 'username'
    template_name = 'blogengine/profile_edit.html'

    def form_valid(self, form):  
        form.save()
        return super().form_valid(form)
