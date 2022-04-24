from .serializers import *
from .models import *
from rest_framework import generics, permissions, status
from django.db.models import Count
from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from time import time


class ListArticle(generics.ListAPIView):
	serializer_class = ArticleSerializer
	queryset = Article.objects.all()


	def get(self, request):
		word_vec = WordVector()
		search_query = request.query_params.get('q', None)

		#get embedding vector for search query and articls
		query_vec = word_vec.get_vector(search_query)
		embeddind = ArticleVector.get_embedding_matrice()
		article_ids = ArticleVector.get_articl_ids()

		#compute corrolation between search query and articles and sort articles base on that
		corrolation = embeddind.dot(query_vec)
		index = corrolation.argsort()
		id_list = article_ids[index][-10:]
		objs = self.get_queryset().filter(id__in=id_list)
		serializer = self.get_serializer(objs, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK )




class TagViewSet(mixins.CreateModelMixin,
				 mixins.RetrieveModelMixin,
				 mixins.ListModelMixin,
				 viewsets.GenericViewSet):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		tag = self.request.query_params.get('name', None)
		queryset = Tag.objects.all()
		if tag is not None:
			return queryset.annotate(count=Count('article'))\
						   .filter(name__regex=r'.*' + tag + r'.*')\
						   .order_by('-count')[:5]
		return queryset


class ListTopic(generics.ListAPIView):
	serializer_class = TopicSerializer

	def get_queryset(self):
		topic = self.request.query_params.get('name', None)
		queryset = Topic.objects.all()
		if topic is not None:
			return queryset.annotate(count=Count('article'))\
						   .filter(name__regex=r'.*' + topic + r'.*')\
						   .order_by('-count')[:5]
		return queryset


	

class RetrieveAuthor(generics.RetrieveAPIView):
	serializer_class = BlogUserSerializer
	permission_classes = [permissions.IsAuthenticated]
	queryset = BlogUser.objects.all()



class ArticleLikeViewSet(mixins.CreateModelMixin,
						 mixins.UpdateModelMixin,
						 mixins.DestroyModelMixin,
						 mixins.RetrieveModelMixin,
						 viewsets.GenericViewSet):
	queryset = ArticleLike.objects.all()
	serializer_class = ArticleLikeSerializer
	permission_classes = [permissions.IsAuthenticated]
	
	def get_object(self):
		queryset = self.get_queryset()
		filter = {}
		for field in ['user', 'article']:
			filter[field] = self.request.query_params.get(field)

		obj = get_object_or_404(queryset, **filter)		
		self.check_object_permissions(self.request, obj)
		return obj



class CommentLikeViewSet(mixins.CreateModelMixin,
						 mixins.UpdateModelMixin,
						 mixins.DestroyModelMixin,
						 viewsets.GenericViewSet):
	queryset = CommentLike.objects.all()
	serializer_class = CommentLikeSerializer
	permission_classes = [permissions.IsAuthenticated]
	
	def get_object(self):
		queryset = self.get_queryset()
		filter = {}
		for field in ['user', 'comment']:
			filter[field] = self.request.query_params.get(field)

		obj = get_object_or_404(queryset, **filter)		
		self.check_object_permissions(self.request, obj)
		return obj
		

class BookmarkViewSet(mixins.CreateModelMixin,
					  mixins.DestroyModelMixin,
					  mixins.RetrieveModelMixin,
					  viewsets.GenericViewSet):
	queryset = Bookmark.objects.all()
	serializer_class = BookmarkSerializer
	permission_classes = [permissions.IsAuthenticated]
	
	def get_object(self):
		queryset = self.get_queryset()
		filter = {}
		for field in ['user', 'article']:
			filter[field] = self.request.query_params.get(field)

		obj = get_object_or_404(queryset, **filter)		
		self.check_object_permissions(self.request, obj)
		return obj


class FollowViewSet(mixins.CreateModelMixin,
					mixins.DestroyModelMixin,
					mixins.ListModelMixin,
					viewsets.GenericViewSet):
	queryset = Follow.objects.all()
	serializer_class = FollowSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		queryset = Follow.objects.all()
		try:
			bloguser = self.request.user.bloguser
			profile = self.request.query_params.get('profile', None)
			if profile is not None:
				return queryset.filter(user=bloguser)
		except:
			pass

	def get_object(self):
		queryset = self.get_queryset()
		filter = {}
		for field in ['user', 'author']:
			filter[field] = self.request.query_params.get(field)

		obj = get_object_or_404(Follow, **filter)		
		self.check_object_permissions(self.request, obj)
		return obj


class CommentViewSet(mixins.CreateModelMixin,
					 mixins.UpdateModelMixin,
					 mixins.ListModelMixin,
					 viewsets.GenericViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticated, ]
	
	def get_queryset(self):
		queryset = Comment.objects.all()
		try:
			bloguser = self.request.user.bloguser
			
			param = {}
			for field in ['profile', 'editor', 'topic']:
				param[field] = self.request.query_params.get(field, None)
			
			if param['profile'] is not None:
				return queryset.filter(user=bloguser)
				
			elif param['editor'] is not None and bloguser.is_editor:
				
				filter = {'is_valid': False}
				
				if param['topic']:
					filter['article__topic'] = param['topic']
				
				return queryset.filter(**filter)
			
		except Exception as e:
			print(e)

class ArticleViewSet(mixins.UpdateModelMixin,
					 mixins.ListModelMixin,
					 viewsets.GenericViewSet):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializer
	permission_classes = [permissions.IsAuthenticated, ]

	def get_queryset(self):
		queryset = Article.objects.all()
		filter = {'is_valid': True, 'is_active': True}
		try:
			bloguser = self.request.user.bloguser
			
			param = {}
			for field in ['profile', 'editor', 'topic', 'bookmark', 'liked']:
				param[field] = self.request.query_params.get(field, None)
			
			if param['profile'] is not None:
				return queryset.filter(author=bloguser)
				
			elif param['editor'] is not None and bloguser.is_editor:
				filter['is_valid'] = False
				
				if param['topic']:
					filter['topic'] = param['topic']
				
				return queryset.filter(**filter)
				
			elif param['bookmark'] is not None:
				return queryset.filter(bookmarkedBy=bloguser, **filter)
				
			elif param['liked'] is not None:
				return queryset.filter(articlelike__is_like=True, user_liked=bloguser, **filter)
				
			else:
				return queryset.filter(**filter)
				
		except Exception as e:
			print(e)
			return queryset.filter(**filter)
		







