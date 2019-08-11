from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from .models import Post, Gallery
from .forms import *

# Create your views here.
def post_list(request):
	posts = Post.objects.all().order_by('-create_at')
	return render(request, 'blogengine/posts_list.html', {'posts': posts})

def post_detail(request, slug):
	post = get_object_or_404(Post, slug__iexact = slug)
	return render(request, 'blogengine/post_detail.html', {'post': post})

class PostCreate(CreateView):
	model = Post
	fields = ['title', 'text']

	def form_valid(self,form):
		new_post = form.save(commit = False)
		new_post.author = self.request.user
		new_post.save()
		print(self.request.FILES.getlist('gallery'))
		for item in self.request.FILES.getlist('gallery'):
			Gallery.objects.create(image = item, thumbnail = item, post = new_post)
		return super().form_valid(form)
		# return redirect('post_detail', slug = new_post.slug)

	def get(self, request):
		form = PostForm()
		title = 'Post create'
		return render(request, 'blogengine/post_create.html',{'form':form, 'title':title})

class PostEdit(UpdateView):
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
			Gallery.objects.create(image = item, post = edit_post)
		return super().form_valid(form)