from django import template

register = template.Library()

@register.filter(name='user_follow_status')
def status(instance, user):
	return instance.user_follow_status(user.bloguser)['follow']
