from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import Group
import pymongo
import numpy
import redis


class Article(models.Model):
	is_vectorized = models.BooleanField(default=False)
	is_active = models.BooleanField('نمایش عمومی؟', default=True)
	is_valid = models.BooleanField('تایید شده؟', default=False)
	pub_date = models.DateTimeField('زمان انتشار', auto_now_add=True)
	val_date = models.DateTimeField('زمان تایید', null=True, blank=True)
	img_path = models.ImageField('محل ذخیره تصویر', upload_to='%Y/%m/%d/', max_length=750)
	title = models.CharField('عنوان مقاله', max_length=350)
	text = models.TextField('متن مقاله', validators=[MinLengthValidator(300)])
	author = models.ForeignKey(
		'BlogUser', on_delete=models.CASCADE, related_name='published', verbose_name='نویسنده')
	validator = models.ForeignKey('BlogUser', on_delete=models.PROTECT, null=True,
		blank=True, related_name='Avalidated', verbose_name='تایید کننده')
	tag = models.ManyToManyField('Tag', blank=True, verbose_name='برچسب')
	topic = models.ForeignKey(
		'Topic', on_delete=models.PROTECT, verbose_name='دسته بندی')
	user_liked = models.ManyToManyField(
		'BlogUser', through='ArticleLike', related_name='alikes', verbose_name='پسند')


	def save(self, *args, **kwargs):
		if self.is_valid and self.val_date is None:
			self.val_date = timezone.now()
		elif not self.is_valid and self.val_date is not None:
			self.val_date = None
		super().save(*args, **kwargs)

	class Meta:
		ordering = ['-pub_date']

	def get_likes(self):
		return self.user_liked.through.objects.filter(is_like=True, article=self).count()

	def get_dislikes(self):
		return self.user_liked.through.objects.filter(is_like=False, article=self).count()

	def user_like_status(self, user):
		try:
			obj = ArticleLike.objects.get(user=user, article=self)
			if obj.is_like == True:
				return {'did_like': True, 
						'is_like': True, 
						'like_count': self.get_likes(), 
						'dislike_count': self.get_dislikes()}
			else:
				return {'did_like': True, 
						'is_like': False, 
						'like_count': self.get_likes(), 
						'dislike_count': self.get_dislikes()}
		except ArticleLike.DoesNotExist:
			return {'did_like': False, 
					'is_like': False, 
					'like_count': self.get_likes(), 
					'dislike_count': self.get_dislikes()}


	def __str__(self):
		return self.title


class Comment(models.Model):
	text = models.CharField('متن نظر', max_length=200)
	is_valid = models.BooleanField('تایید شده؟', default=False)
	pub_date = models.DateTimeField('زمان انتشار', auto_now_add=True)
	val_date = models.DateTimeField('زمان تایید', null=True, blank=True)
	user = models.ForeignKey('BlogUser', on_delete=models.CASCADE,
	related_name='comments', verbose_name='نویسنده')
	validator = models.ForeignKey('BlogUser', on_delete=models.PROTECT, null=True,
		blank=True, related_name='Cvalidated', verbose_name='تایید کننده')
	article = models.ForeignKey(
		'Article', on_delete=models.CASCADE, verbose_name='مقاله')
	response_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
		blank=True, related_name='response', verbose_name='پاسخ به')
	user_liked = models.ManyToManyField(
		'BlogUser', through='CommentLike', related_name='clikes', verbose_name='پسند')

	def save(self, *args, **kwargs):
		if self.is_valid and self.val_date is None:
			self.val_date = timezone.now()
		elif not self.is_valid and self.val_date is not None:
			self.val_date = None
		super().save(*args, **kwargs)

	def get_likes(self):
		return self.user_liked.through.objects.filter(is_like=True, comment=self).count()

	def get_dislikes(self):
		return self.user_liked.through.objects.filter(is_like=False, comment=self).count()

	def get_responses(self):
		return self.response.all().values_list('text')

	def __str__(self):
		return self.text

	def user_like_status(self, user):
		try:
			obj = CommentLike.objects.get(user=user, comment=self)
			if obj.is_like == True:
				return {'did_like': True, 
						'is_like': True, 
						'like_count': self.get_likes(), 
						'dislike_count': self.get_dislikes()}
			else:
				return {'did_like': True, 
						'is_like': False, 
						'like_count': self.get_likes(), 
						'dislike_count': self.get_dislikes()}
		except CommentLike.DoesNotExist:
			return {'did_like': False, 
					'is_like': False, 
					'like_count': self.get_likes(), 
					'dislike_count': self.get_dislikes()}


class BlogUser(User):

	def user_directory_path(self, filename):
		return f'user/user_{self.id}/{filename}'

	phone_number = models.CharField('شماره تلفن', max_length=11)
	img_path = models.ImageField('محل ذخیره عکس', upload_to=user_directory_path)
	is_author = models.BooleanField('نویسنده است؟', default=False)
	is_editor = models.BooleanField('ویراستار است؟', default=False)
	is_manager = models.BooleanField('مدیر است؟', default=False)
	is_inactive = models.BooleanField('غیر فعال شده؟', default=False)
	followers = models.ManyToManyField(
		'self', symmetrical=False, through='Follow', related_name='followedBy', verbose_name='دنبال کردن')
	bookmarked_articles = models.ManyToManyField(
		'Article', through='Bookmark', related_name='bookmarkedBy', verbose_name='نشان کردن')
	bio = models.CharField('درباره من', max_length=250)

	def save(self, *args, **kwargs):
		if self.is_manager:
			self.groups.add(Group.objects.get(name='managers'))

		super().save(*args, **kwargs)

	def __str__(self):
		return self.username

	def full_name(self):
		return self.first_name + ' ' + self.last_name

	def user_follow_status(self, user):
		try:
			obj = Follow.objects.get(author=self, user=user)
			return {'follow': True, 'followers': self.followedBy.count()}
		except Follow.DoesNotExist:
			return {'follow': False, 'followers': self.followedBy.count()}


class Tag(models.Model):
	name = models.CharField('برچسب', max_length=55, unique=True)

	def __str__(self):
		return self.name


class Topic(models.Model):
	name = models.CharField('دسته بندی', max_length=55)
	super_topic = models.ForeignKey(
		'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subtopics', verbose_name='فرا مجموعه')

	def __str__(self):
		return self.name


class ArticleLike(models.Model):
	article = models.ForeignKey(
		'Article', on_delete=models.CASCADE, verbose_name='مقاله')
	user = models.ForeignKey(
		'BlogUser', on_delete=models.CASCADE, verbose_name='کاربر')
	is_like = models.BooleanField('پسند؟', default=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(
			fields=['article', 'user'], name='article_like')
		]

	def __str__(self):
		return self.user.username + '، ' + self.article.title + ("پسندید." if self.is_like else 'نپسندید.')


class CommentLike(models.Model):
	comment = models.ForeignKey(
		'Comment', on_delete=models.CASCADE, verbose_name='نظر')
	user = models.ForeignKey(
		'BlogUser', on_delete=models.CASCADE, verbose_name='کاربر')
	is_like = models.BooleanField('پسند؟', default=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(
			fields=['comment', 'user'], name='comment_like')
		]


	def __str__(self):
		return self.user.username + '، ' + self.comment.text + ("پسندید." if self.is_like else 'نپسندید.')


class Follow(models.Model):
	author = models.ForeignKey(
		'BlogUser', on_delete=models.CASCADE, related_name='follower', verbose_name='نویسنده')
	user = models.ForeignKey('BlogUser', on_delete=models.CASCADE,
	related_name='following', verbose_name='کاربر')

	class Meta:
		constraints = [
		models.UniqueConstraint(fields=['author', 'user'], name='follow')
		]

	def __str__(self):
		return self.user.username + '، ' + self.author.username + "را دنبال کرد."


class Bookmark(models.Model):
	article = models.ForeignKey(
		'Article', on_delete=models.CASCADE, related_name='bookmarkers', verbose_name='مقاله')
	user = models.ForeignKey('BlogUser', on_delete=models.CASCADE,
		related_name='bookmarks', verbose_name='کاربر')

	class Meta:
		constraints = [
			models.UniqueConstraint(
			fields=['article', 'user'], name='bookmark')
		]

	def __str__(self):
		return self.user.username + '، ' + self.article.title + "را نشان کرد."


class ArticleVector(models.Model):
	article = models.OneToOneField(
		Article,
		on_delete=models.CASCADE,
		primary_key=True,
	)

	embedding = ArrayField(
		models.FloatField(),
		size=100
	)
	
	@classmethod
	def get_embedding_matrice(clf):
		return numpy.array(clf.objects.values_list('embedding', flat=True))

	@classmethod
	def get_articl_ids(clf):
		return numpy.array(clf.objects.values_list('article', flat=True))

myclient = pymongo.MongoClient()
mydb = myclient["word2vec"]
#R = redis.Redis(decode_responses=True)


class WordVector:
	def __init__(self):
		self.collection = mydb["words"]

	def _get_word(self, word):
		return self.collection.find_one({"word": word})

	def _get_unknown_by_length(self, word):
		word_length = len(word)
		vec_list = self.collection.distinct('vector', {'$where': 'this.word.length == {word_length}'})
		return numpy.mean(vec_list, axis=0).tolist()


	def _get_word_vector(self, word):
		dic = self._get_word(word)

		if dic is not None:
			return numpy.array(dic["vector"])

#		if not R.exists(f'unknown_{len(word)}'):
#			R.rpush(f'unknown_{len(word)}', *self._get_unknown_by_length(word))

#		return numpy.array(R.lrange(f'unknown_{len(word)}'), dtype='float32')

	def get_vector(self, query):
		words = query.split()

		return numpy.mean([self._get_word_vector(word) for word in words], axis=0)












