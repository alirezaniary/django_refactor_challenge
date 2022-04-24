from django.shortcuts import render
from blog.models import Topic, Article, Comment
from django.db.models import Count
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
	topic_list = Topic.objects.filter(super_topic=None)
	art_not_validated = Article.objects.filter(is_valid=False).count()
	art_per_topic = Topic.objects.filter(article__is_valid=False).annotate(count=Count('article'))
	com_not_validated = Comment.objects.filter(is_valid=False).count()
	com_per_topic = Topic.objects.filter(article__comment__is_valid=False).annotate(count=Count('article__comment'))
	filter = {'is_valid': True, 'is_active': True}
	liked_article = Article.objects.filter(articlelike__is_like=True, user_liked=request.user, **filter).count()
	return render(request, 'registration/profile.html',{'topic_list': topic_list,
														'art_count': art_not_validated,
														'art_per_topic': art_per_topic,
														'com_count': com_not_validated,
														'com_per_topic': com_per_topic,
														'liked_article': liked_article})
	
