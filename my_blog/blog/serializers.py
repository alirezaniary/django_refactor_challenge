from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

class TagSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Tag
		fields = ['id', 'name']
		validators = [
			UniqueValidator(
				queryset=Tag.objects.all()
			)
		]
	
	def validate_name(self, value):
		request = self.context.get('request')
		if request.user.is_author:
			return value

class TopicSerializer(serializers.ModelSerializer):
	def to_representation(self, value):
		return value.name

	class Meta:
		model = Topic
		fields = ['id', 'name']
		validators = [
			UniqueValidator(
				queryset=Topic.objects.all()
			)
		]
		

class TopicSerializer(serializers.ModelSerializer):
	def to_representation(self, value):
		return value.name

	class Meta:
		model = Topic
		fields = ['id', 'name']


class BlogUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = BlogUser
		fields = ['id', 'full_name', 'bio', 'img_path', 'publications', 'followers', 'username']
	publications = serializers.SerializerMethodField()
	followers =  serializers.SerializerMethodField()
	img_path = serializers.SerializerMethodField()

	def get_img_path(self, author):
		request = self.context.get('request')
		try:
			img_path = author.img_path.url
			return request.build_absolute_uri('/media/' + img_path)
		except:
			return request.build_absolute_uri('/static/blog/profile_picture_placeholder.jpeg')

	def get_followers(self, author):
		return author.followedBy.count()

	def get_publications(self, author):
		return author.published.count()


class CommentSerializer(serializers.ModelSerializer):
	article_link = serializers.SerializerMethodField()
	article_title = serializers.SerializerMethodField()
	class Meta:
		model = Comment
		fields = ['id', 'text', 'user', 'article', 'response_to', 'pub_date',
				  'is_valid', 'validator', 'article_link', 'article_title']
		read_only_fields = ['pub_date', 'article_link', 'article_title']
		extra_kwargs = {'validator': {'write_only': True}}
	
	def get_article_link(self, comment):
		username = comment.article.author.username
		article_id = comment.article.id
		request = self.context.get('request')
		return request.build_absolute_uri(f'/@{username}/{article_id}/')
	
	def get_article_title(self, comment):
		return comment.article.title
		
	def validate_validator(self, value):
		article = self.instance
		request = self.context.get('request')
		
		if value == article.user:
			raise serializers.ValidationError("شما قادر به تایید نظر خود نیستید!!")
		
		elif request.user.bloguser != value:
			raise serializers.ValidationError("اطلاعات صحیح نیست!!")
		
		return value


	def validate_is_valid(self, value):
		data = self.get_initial()
		if 'validator' not in data.keys():
			return False
		elif 'text' in data.keys():
			raise serializers.ValidationError("اطلاعات صحیح نیست!!")
		return value
			
		
class FollowSerializer(serializers.ModelSerializer):
	class Meta:
		model = Follow
		fields = ['id', 'user', 'author']


class ArticleLikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ArticleLike
		fields = ['id', 'user', 'article', 'is_like']
		
		validators = [
			UniqueTogetherValidator(
				queryset=ArticleLike.objects.all(),
				fields=['user', 'article']
			)
		]


class BookmarkSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bookmark
		fields = ['id', 'article', 'user']
		
		validators = [
			UniqueTogetherValidator(
				queryset=Bookmark.objects.all(),
				fields=['user', 'article']
			)
		]


class CommentLikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommentLike
		fields = ['id', 'user', 'comment', 'is_like']
		
		validators = [
			UniqueTogetherValidator(
				queryset=CommentLike.objects.all(),
				fields=['user', 'comment']
			)
		]


class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = ['id', 'username', 'author', 'title', 'text', 'is_valid', 'is_active',
				  'img_path', 'validator', 'val_date', 'tag', 'topic']
				  
		read_only_fields = ['author', 'username', 'title', 'text', 'img_path', 'tag', 'topic']
		extra_kwargs = {'validator': {'write_only': True}}

	tag = TagSerializer(many=True,read_only=True)
	topic = TopicSerializer(read_only=True)

	img_path = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()


	def get_img_path(self, article):
		request = self.context.get('request')
		if 'http' in article.img_path.name:
			return article.img_path.name
		img_path = article.img_path.name
		return request.build_absolute_uri('/media/' + img_path)
	
	
	def get_username(self, article):
		return article.author.username
			
		
	def validate_validator(self, value):
		article = self.instance
		request = self.context.get('request')
		if value == article.author:
			raise serializers.ValidationError("شما قادر به تایید مقاله خود نیستید!!")
		
		elif request.user.bloguser != value:
			raise serializers.ValidationError("اطلاعات صحیح نیست!!")
		return value
		
		
	def validate_is_active(self, value):
		article = self.instance
		request = self.context.get('request')
		if request.user.bloguser != article.author:
			raise serializers.ValidationError("شما قادر به تغییر مقاله دیگران نیستید!!")
		return value

	
	def validate_is_valid(self, value):
		data = self.get_initial()
		try:
			data['validator']
		except:
			raise serializers.ValidationError("اطلاعات کافی نیست!!")
		return value






