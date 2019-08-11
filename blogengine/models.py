from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image
import uuid

def generate_slug(string):
	new_slug = slugify(string, allow_unicode=True)
	return new_slug+'-'+str(int(timezone.now().timestamp()))

def generate_path_image(instance, filename):
	time_now = timezone.now()
	ext=filename.split('.')[-1]
	filename = '.'.join([str(uuid.uuid4()),str(ext)])
	image_path = '/'.join(['media','post_images',str(time_now.year),str(time_now.month),str(time_now.day),str(instance.post.slug),str(filename)])
	return image_path

def generate_path_image_thumbnail(instance, filename):
	time_now = timezone.now()
	ext=filename.split('.')[-1]
	filename = '.'.join([str(uuid.uuid4()),str(ext)])
	image_path = '/'.join(['media','post_images',str(time_now.year),str(time_now.month),str(time_now.day) ,str(instance.post.slug),'thumbnail',str(filename)])
	return image_path


class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
	title = models.CharField(max_length = 100)
	text = models.TextField()
	slug = models.SlugField(max_length=150, blank = True)
	create_at = models.DateTimeField(auto_now_add = True)

	def get_absolute_url(self):
		return reverse('post_detail', kwargs = {'slug': self.slug})

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug=generate_slug(self.title)
		super().save(*args, **kwargs)

class Gallery(models.Model):
	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='gallery')
	image = models.ImageField(upload_to = generate_path_image, null = True, blank = True)
	thumbnail = models.ImageField(upload_to = generate_path_image_thumbnail, editable = False)

	def save(self, *args, **kwargs):
		super(Gallery, self).save()
		image = Image.open(self.image.path)
		(width, heigth) = image.size
		if width <= 800:
			factor = 1
		else:
			factor = width/heigth
			print(factor)
			width = 800
			heigth = width/factor
		size = (int(width), int(heigth))
		image = image.resize(size, Image.ANTIALIAS)
		image.save(self.image.path)
		thumb = Image.open(self.thumbnail.path)
		thumb_factor = 8
		thumb_size = (int(width/thumb_factor), int(heigth/thumb_factor))
		thumb = thumb.resize(thumb_size, Image.ANTIALIAS)
		thumb.save(self.thumbnail.path)

