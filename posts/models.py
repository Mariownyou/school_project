from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=25, unique=True, blank=False, null=False)
    description = models.TextField()

    def __str__(self):
        return self.title


class Category(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='category',
        verbose_name='Категории',
        help_text='Выберите Группу'
    )
    slug = models.SlugField(
        max_length=25, unique=True, blank=False, null=False,
        verbose_name='уникальное имя',
        help_text='Уникальное название связанное с заголовком. Используйте латинские буквы. Пробелы заменяйте "-"'
    )
    title = models.CharField(
        max_length=200, unique=True,
        verbose_name='Заголовок',
        help_text='Назовите категорию'
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Ваш пост',
        help_text='Напишите ваш замечательный пост ❤'
    )
    title = models.CharField(
        'Заголовок',
        max_length=200, unique=True,
    )
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True, null=True,
        verbose_name='Категория',
        help_text='Выберите категорию, если хотите 😉'
    )
    is_important = models.BooleanField(
        'Новость?',
        default=False,
        help_text='Поставте галочку если хотите отметить это важным',
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True, null=True,
        verbose_name='Картинка',
        help_text='Картинка украсит ваш пост'
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        author = self.author
        pub_date = self.pub_date
        text = self.text[50:]
        text_to_print = f'{author}\n{pub_date:%Y-%m-%d %H:%M}\n{text}'
        return text_to_print


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Ваш комментарий', help_text='Напишите ваш коммент ❤')
    created = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        post = self.post
        author = self.author
        text = self.text[50:]
        date = self.created
        text_to_print = f'{post}\n{author}\n{text}\n{date:%Y-%m-%d %H:%M}'
        return text_to_print


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', null=True)

    class Meta:
        unique_together = ['user', 'author']
