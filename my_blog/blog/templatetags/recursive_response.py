from django import template
from blog.models import Comment

register = template.Library()

@register.filter(name='recursive_response')
def recursive(value):
	res = []
	def response(com):
		res.append(com)
		for c in com.response.filter(is_valid=True):
			if isinstance(c, Comment):
				response(c)
	response(value)
	return res

