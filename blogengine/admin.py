from django.contrib import admin
from .models import Post, Gallery

class ImageInLine(admin.TabularInline):
	model = Gallery

class PostAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'create_at',)
	inlines = [ImageInLine]

# Register your models here.
admin.site.register(Post, PostAdmin)

