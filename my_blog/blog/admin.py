from .models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class ArticleAdmin(admin.ModelAdmin):
	list_display = ('author', 
					'title', 
					'is_valid', 
					'is_active', 
					'pub_date')


class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 
					'article', 
					'pub_date', 
					'is_valid')


class BlogUserAdmin(admin.ModelAdmin):
	list_display = ('username', 
					'email', 
					'is_author', 
					'is_editor', 
					'is_inactive',)
	readonly_fields = [
		'date_joined',
		'last_login',
	]

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		is_superuser = request.user.is_superuser

		disabled_fields = set() 

		if not is_superuser:
			disabled_fields |= {
				'is_superuser', 
				'groups', 
				'user_permissions',
				'is_staff',
				'is_active',
				'username',
				}
		# Prevent non-superusers from editing their own permissions
		if (
			not is_superuser
			and obj is not None
			and obj == request.user
			):
			disabled_fields |= {
				'is_staff',
				'is_superuser',
				'groups',
				'user_permissions',
			}
		for f in disabled_fields:
			if f in form.base_fields:
				form.base_fields[f].disabled = True

		return form


class TagAdmin(admin.ModelAdmin):
	list_display = ('name',)
	

class TopicAdmin(admin.ModelAdmin):
	list_display = ('name', 'super_topic')	

admin.site.unregister(User)
#admin.site.register(User, UserAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(BlogUser, BlogUserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Tag, TagAdmin)
#admin.site.register(ArticleLike)
