from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Gallery, User

class ImageInLine(admin.TabularInline):
	model = Gallery

class PostAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'create_at',)
	inlines = [ImageInLine]

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)


