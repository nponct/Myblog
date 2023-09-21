from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=70, unique=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category',kwargs={'cat_slug':self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class ArtPost(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.PROTECT,null=True, verbose_name="Категория")
    title = models.CharField(max_length=70, verbose_name="Тема поста")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    author = models.ForeignKey(User, verbose_name="Автор поста",on_delete=models.CASCADE)
    content = models.TextField(max_length=3000, verbose_name="Содержание")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Comment(models.Model):
    commentpost = models.ForeignKey(ArtPost, verbose_name="Пост", on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=70, verbose_name="Тема поста")
    content = models.TextField(max_length=3000, verbose_name="Текст сообщения")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', verbose_name="Исходный пост", on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['-time_create']
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return str(self.author) + ' comment ' + str(self.content)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False







