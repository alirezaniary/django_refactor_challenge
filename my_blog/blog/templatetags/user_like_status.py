from django import template

register = template.Library()

@register.filter(name='user_like_status')
def status(instance, user):
	st = instance.user_like_status(user.bloguser)
	
	if st['did_like'] == True and st['is_like'] == True:
		return {'lf':False, 'le':True, 'df':True, 'de':False}
		
	elif st['did_like'] == True and st['is_like'] == False:
		return {'lf':True, 'le':False, 'df':False, 'de':True}
		
	elif st['did_like'] == False and st['is_like'] == False:
		return {'lf':True, 'le':False, 'df':True, 'de':False}
