# Generated by Django 3.1.7 on 2022-04-24 17:30

import blog.models
import django.contrib.auth.models
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_vectorized', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True, verbose_name='نمایش عمومی؟')),
                ('is_valid', models.BooleanField(default=False, verbose_name='تایید شده؟')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')),
                ('val_date', models.DateTimeField(blank=True, null=True, verbose_name='زمان تایید')),
                ('img_path', models.ImageField(max_length=750, upload_to='%Y/%m/%d/', verbose_name='محل ذخیره تصویر')),
                ('title', models.CharField(max_length=350, verbose_name='عنوان مقاله')),
                ('text', models.TextField(validators=[django.core.validators.MinLengthValidator(300)], verbose_name='متن مقاله')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='BlogUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('phone_number', models.CharField(max_length=11, verbose_name='شماره تلفن')),
                ('img_path', models.ImageField(upload_to=blog.models.BlogUser.user_directory_path, verbose_name='محل ذخیره عکس')),
                ('is_author', models.BooleanField(default=False, verbose_name='نویسنده است؟')),
                ('is_editor', models.BooleanField(default=False, verbose_name='ویراستار است؟')),
                ('is_manager', models.BooleanField(default=False, verbose_name='مدیر است؟')),
                ('is_inactive', models.BooleanField(default=False, verbose_name='غیر فعال شده؟')),
                ('bio', models.CharField(max_length=250, verbose_name='درباره من')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, verbose_name='متن نظر')),
                ('is_valid', models.BooleanField(default=False, verbose_name='تایید شده؟')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')),
                ('val_date', models.DateTimeField(blank=True, null=True, verbose_name='زمان تایید')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article', verbose_name='مقاله')),
                ('response_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='response', to='blog.comment', verbose_name='پاسخ به')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.bloguser', verbose_name='نویسنده')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, unique=True, verbose_name='برچسب')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleVector',
            fields=[
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='blog.article')),
                ('embedding', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=100)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, verbose_name='دسته بندی')),
                ('super_topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subtopics', to='blog.topic', verbose_name='فرا مجموعه')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='blog.bloguser', verbose_name='نویسنده')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='blog.bloguser', verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=True, verbose_name='پسند؟')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.comment', verbose_name='نظر')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.bloguser', verbose_name='کاربر')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='user_liked',
            field=models.ManyToManyField(related_name='clikes', through='blog.CommentLike', to='blog.BlogUser', verbose_name='پسند'),
        ),
        migrations.AddField(
            model_name='comment',
            name='validator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Cvalidated', to='blog.bloguser', verbose_name='تایید کننده'),
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarkers', to='blog.article', verbose_name='مقاله')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='blog.bloguser', verbose_name='کاربر')),
            ],
        ),
        migrations.AddField(
            model_name='bloguser',
            name='bookmarked_articles',
            field=models.ManyToManyField(related_name='bookmarkedBy', through='blog.Bookmark', to='blog.Article', verbose_name='نشان کردن'),
        ),
        migrations.AddField(
            model_name='bloguser',
            name='followers',
            field=models.ManyToManyField(related_name='followedBy', through='blog.Follow', to='blog.BlogUser', verbose_name='دنبال کردن'),
        ),
        migrations.CreateModel(
            name='ArticleLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=True, verbose_name='پسند؟')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article', verbose_name='مقاله')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.bloguser', verbose_name='کاربر')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='published', to='blog.bloguser', verbose_name='نویسنده'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(blank=True, to='blog.Tag', verbose_name='برچسب'),
        ),
        migrations.AddField(
            model_name='article',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.topic', verbose_name='دسته بندی'),
        ),
        migrations.AddField(
            model_name='article',
            name='user_liked',
            field=models.ManyToManyField(related_name='alikes', through='blog.ArticleLike', to='blog.BlogUser', verbose_name='پسند'),
        ),
        migrations.AddField(
            model_name='article',
            name='validator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Avalidated', to='blog.bloguser', verbose_name='تایید کننده'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('author', 'user'), name='follow'),
        ),
        migrations.AddConstraint(
            model_name='commentlike',
            constraint=models.UniqueConstraint(fields=('comment', 'user'), name='comment_like'),
        ),
        migrations.AddConstraint(
            model_name='bookmark',
            constraint=models.UniqueConstraint(fields=('article', 'user'), name='bookmark'),
        ),
        migrations.AddConstraint(
            model_name='articlelike',
            constraint=models.UniqueConstraint(fields=('article', 'user'), name='article_like'),
        ),
    ]
