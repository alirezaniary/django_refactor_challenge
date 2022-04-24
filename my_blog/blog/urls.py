from django.urls import path, re_path, include
from django.views.static import serve
from . import views
from django.conf import settings

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('new/', views.new_article, name='new_article'),
    path('@<str:username>/<int:article_id>/', views.show_article, name='article'),
    path('@<str:username>/', views.show_publication, name='publication'),
    path('<int:pk>/edit/', views.edit_article, name='edit_article'),
    path('api/', include('blog.API_urls')),
    path('tags/<str:tag_name>/', views.show_tag, name='tags'),
    path('topics/<str:topic_name>/', views.show_topic, name='topics'),
]


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
