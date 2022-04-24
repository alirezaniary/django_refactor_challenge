from django.urls import path, include
from blog.APIs import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('like', ArticleLikeViewSet)
router.register('clike', CommentLikeViewSet)
router.register('bookmark', BookmarkViewSet)
router.register('comment', CommentViewSet)
router.register('article', ArticleViewSet)
router.register('follow', FollowViewSet)
router.register('tag', TagViewSet),


urlpatterns = [
	path('', include(router.urls)),
	path('author/<int:pk>/', RetrieveAuthor.as_view()),
	path('search/', ListArticle.as_view()),
	path('topic/', ListTopic.as_view()),
]

