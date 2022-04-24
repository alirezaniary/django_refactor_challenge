from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, ArticleCreationForm, CommentForm
from django.views import generic
from .models import BlogUser, Article, Topic, Tag
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required


topic_list = Topic.objects.filter(super_topic=None)

def index(request):
    page = request.GET.get('page', None)
    try:
        if page and int(page) > 1:
            page = int(page)
            queryset =  Article.objects.filter(is_valid=True, is_active=True)[(page-1)*10: page*10]
        else:
            page = 1
            queryset =  Article.objects.filter(is_valid=True, is_active=True)[0:10]
        return render(request, 'index.html',{'topic_list': topic_list,
        									 'article': queryset,
        									 'page': page})
    except:
        return render(request, 'index.html',{'topic_list': topic_list,
        									 'article': Article.objects.filter(is_valid=True, is_active=True)[0:10]
        									 })

def show_publication(request, username):
    page = request.GET.get('page', None)
    try:
        if page and int(page) > 1:
            page = int(page)
            queryset =  Article.objects.filter(is_valid=True, is_active=True, author__username=username)[(page-1)*10: page*10]
        else:
            page = 1
            queryset =  Article.objects.filter(is_valid=True, is_active=True, author__username=username)[0:10]
        return render(request, 'index.html',{'topic_list': topic_list,
        									 'article': queryset,
        									 'page': page})
    except:
        return render(request, 'index.html',{'topic_list': topic_list,
        									 'article': Article.objects.filter(is_valid=True, is_active=True, author__username=username)[0:10]
        									 })
        									 

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('blog:index')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form,
                                            'topic_list': topic_list
                                            })

@login_required
def new_article(request):
    if request.method == 'POST' and request.user.bloguser.is_author:
        article_form = ArticleCreationForm(request.POST, request.FILES)

        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.author_id = request.user.bloguser.id
            article.save()
            article_form.save_m2m()
            return redirect('blog:article',
            				article_id=article.id,
            				username=request.user.username)
        else:
            render(request, 'new_article.html', {'form': article_form,
                                                'topic_list': topic_list,
                                                })
    elif request.method == 'GET' and request.user.bloguser.is_author:
        article_form = ArticleCreationForm()
    return render(request, 'new_article.html', {'form': article_form,
                                                'topic_list': topic_list,

                                                })


def show_article(request, username, article_id):
	article = get_object_or_404(
	    Article, pk=article_id, author__username=username)
	author = article.author
	comments = article.comment_set.filter(response_to=None, is_valid=True)
	article_count = author.published.filter(is_valid=True).count()
	follower_count = author.followers.count()
	comment_form = CommentForm()
	return render(request,
				 'show_article.html',
				 {'author': author, 
				  'article': article,
				  'article_count': article_count,
				  'follower_count': follower_count,
				  'topic_list': topic_list, 
				  'form': comment_form,
				  'comments': comments,
				  'data': {'article': article.id,
				  		   'author': author.id,
				  		   'user': request.user.bloguser.id if request.user.is_authenticated else None}
				 })

def show_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    page = request.GET.get('page', None)
    try:
        if page and int(page) > 1:
            page = int(page)
            queryset =  Article.objects.filter(is_valid=True,
            								   is_active=True,
            								   tag__name=tag_name)[(page-1)*10: page*10]
        else:
            page = 1
            queryset =  Article.objects.filter(is_valid=True,
            								   is_active=True,
            								   tag__name=tag_name)[0:10]
            								   
        return render(request, 'index.html',{'topic_list': topic_list,
											 'article': queryset,
											 'title': tag,
											 'page': page
		                                     })
    except:
        return render(request, 'index.html',{'topic_list': topic_list,
											 'article': Article.objects.filter(is_valid=True,
																    		   is_active=True,
																   			   tag__name=tag_name)[0:10],
											 'title': tag
		                                     })


def show_topic(request, topic_name):
    topic = get_object_or_404(Topic, name=topic_name)
    page = request.GET.get('page', None)
    try:
        if page and int(page) > 1:
            page = int(page)
            queryset =  Article.objects.filter(is_valid=True,
            								   is_active=True,
            								   topic__name=topic_name)[(page-1)*10: page*10]
        else:
            page = 1
            queryset =  Article.objects.filter(is_valid=True,
            								   is_active=True,
            								   topic__name=topic_name)[0:10]
            								   
        return render(request, 'index.html',{'topic_list': topic_list,
											 'article': queryset,
											 'title': topic,
											 'page': page
		                                     })
    except:
        return render(request, 'index.html',{'topic_list': topic_list,
											 'article': Article.objects.filter(is_valid=True,
																    		   is_active=True,
																   			   topic__name=topic_name)[0:10],
											 'title': topic
		                                     })


@login_required
class ArticleUpdateView(UpdateView):
	model = Article
	fields = ('title', 
			  'text',
			  'img_path', 
			  'tag', 
			  'topic', 
			  'is_active', 
			  'is_valid')
	template_name = 'article_form.html'
	success_url ="/"


@login_required
def edit_article(request, pk):
	article = get_object_or_404(Article, pk=pk)
	print(article)
	form = ArticleCreationForm(instance=article)
	print(form)
	return render(request, 'article_form.html',{'topic_list': topic_list,
												'form': form,
				                                 })







