from django.http import HttpResponse #Заменить
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from .models import Post, Gallery, Comment
from .forms import *
from .token import account_activation_token

# Create your views here.
def post_list(request):
    posts = Post.objects.all().order_by('-create_at')
    return render(request, 'blogengine/posts_list.html', {'posts': posts})


class CommentDelete(LoginRequiredMixin, DeleteView):
    #используя модель Comment, удаляю комментарий без использования дополнительных шаблонов с помощью
    #метода get
    model = Comment
    success_url = '/'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug__iexact = kwargs['slug'])
        comment = Comment.objects.get(id=kwargs['id'])
        comment.delete()
        return redirect('post_detail', post.slug)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blogengine/post_detail.html'


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


class RegistrationFormView(FormView):
    form_class = RegisterForm
    success_url = '/accounts/login/'
    template_name = 'blogengine/registration.html'

    def form_valid(self, form):
        #Устанавливаем флаг is_active False для отправки активационного письма 
        user = form.save(commit = False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account'
        message = render_to_string('registration/account_activate_email.html',{
                'user': user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        to_email = form.cleaned_data['email']
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()


        # recipient_list=form.cleaned_data['email']
        # registration_email(self.request, recipient_list)
        return super(RegistrationFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegistrationFormView, self).form_invalid(form)


class ProfileView(DetailView):
    model = User
    template_name = 'blogengine/profile.html'
    slug_field = 'username'

    def get(self, request, *args, **kwargs):
        profile_nickname = str(self.request.path).rsplit('/', maxsplit=2)[1]
        profile = get_object_or_404(User, username=profile_nickname)
        return render(request, 'blogengine/profile.html', {'profile':profile})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('userImage','bio')
    slug_field = 'username'
    template_name = 'blogengine/profile_edit.html'

    def get(self, request, *args, **kwargs):
        #проверяем по никнейму пользователя
        profile_nickname = str(self.request.path).rsplit('/', maxsplit=3)[1]
        if str(request.user)==profile_nickname:
            profile_edit = get_object_or_404(User, username=profile_nickname)
            return render(request, 'blogengine/profile_edit.html', {'profile':profile_edit})
        else:
            return redirect('posts_list')

    def form_valid(self, form):  
        form.save()
        return super().form_valid(form)

# def registration_email(request, recipient):
#     subject = 'Thank you for registering on my site'
#     message = "Now it's testing email"
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = []
#     recipient_list.append(recipient)
#     send_mail( subject, message, email_from, recipient_list)
#     return redirect('posts_list')

def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('posts_list')
    else:
        return HttpResponse('Activation link is invalid!')