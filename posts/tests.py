from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Comment, Follow, Group, Post, User


class PostsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.c = Client()
        self.user = User.objects.create_user(
            username='dina',
        )
        self.client.force_login(self.user)
        self.group = Group.objects.create(
            slug='group1',
            title='g1',
            description='very cool group'
        )
        self.new_group = Group.objects.create(
            slug='group2',
            title='g2',
            description='very cool group2'
        )
        cache.clear()
    
    def tearDown(self):
        key = make_template_fragment_key('index_page')
        cache.delete(key)

    def _check_posts(self, responses, text, group, count=1):
        post = Post.objects.first()
        for r in responses:
            with self.subTest(r=r):
                response = self.client.get(r)
                paginator = response.context.get('paginator')
                self.assertEqual(response.status_code, 200)

                if paginator:
                    self.assertIn('page', response.context)
                    posts = response.context.get('page')
                    self.assertEqual(paginator.count, count)
                    if count > 0:
                        self.assertEqual(post, posts[0])
                else:
                    self.assertIn('post', response.context)
                    page_post = response.context['post']
                    self.assertEqual(post, page_post)
                if count > 0:
                    self.assertEqual(post.text, text)
                    self.assertEqual(post.group, group)

    def test_create_profile(self):
        """После регистрации пользователя создается его персональная страница (profile)"""
        response = self.client.get(reverse('profile', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        """Авторизованный пользователь может опубликовать пост (new)."""
        response = self.client.post(reverse('new'), data={'text': 'test text', 'group': self.group.id}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        test_text = 'test text'
        self.assertEqual(test_text, post.text)
        self.assertEqual(self.group, post.group)
        self.assertEqual(self.user, post.author)

    def test_new_post_not_auth(self):
        """Неавторизованный посетитель не может опубликовать пост
        (его редиректит на страницу входа)."""
        response = self.c.post(
                        reverse('new'),
                        data={'text': 'text', 'group': self.group.id},
                        follow=True)
        self.assertEqual(response.status_code, 200)
        login_url = reverse('login')
        new_post_url = reverse('new')
        target_url = f'{login_url}?next={new_post_url}'
        self.assertRedirects(response, target_url)
        self.assertEqual(Post.objects.count(), 0)

    def test_after_post(self):
        """После публикации поста:"""
        username = self.user.username
        post = Post.objects.create(
            text='text_old',
            group=self.group,
            author=self.user
        )

        responses = [
            reverse('index'),
            reverse('post', kwargs={'username': username, 'post_id': post.id}),
            reverse('profile', kwargs={'username': username})
        ]
        self._check_posts(responses, 'text_old', self.group)

    def test_after_edit_post(self):
        """Авторизованный пользователь может отредактировать свой пост
        и его содержимое изменится на всех связанных страницах"""
        text_old = 'text old'
        text_new = 'text'
        username = self.user.username
        self.client.force_login(self.user)

        # создаем пост
        post = Post.objects.create(
            text=text_old,
            group=self.group,
            author=self.user
        )
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()

        # изменяем пост
        self.client.post(
            reverse(
                    'post_edit',
                    kwargs={'username': username, 'post_id': post.id}
                    ),
            data={'text': text_new, 'group': self.new_group.id},
            follow=True
        )

        responses = [
            reverse('index'),
            reverse('profile', kwargs={'username': username}),
            reverse('post', kwargs={'username': username, 'post_id': post.pk}),
            reverse('group', kwargs={'slug': self.new_group.slug})
        ]
        self._check_posts(responses, text_new, self.new_group)

    def test_404_error(self):
        '''Тест 404 ошибки'''
        response = self.client.get('/404errorpagewhichidonthave', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_post_with_image(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        img = SimpleUploadedFile(
            name='some.gif',
            content=small_gif,
            content_type='image/gif',
        )
        post = Post.objects.create(
            author=self.user,
            text='text',
            group=self.group,
            image=img
        )
        responses = [
            reverse('profile', kwargs={'username': self.user.username}),
            reverse('index'),
            reverse('group', kwargs={'slug': self.group.slug}),
            reverse('post', kwargs={'username': self.user.username, 'post_id': post.id})
        ]
        for url in responses:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, '<img')

    def test_post_without_image(self):
        not_img = SimpleUploadedFile(
            name='some.txt',
            content=b'abc',
            content_type='text/plain',
        )
        url = reverse('new')
        response = self.client.post(url, {'text': 'text', 'image': not_img})
        self.assertFormError(
            response,
            'form',
            'image',
            errors='Загрузите правильное изображение. Файл, который вы загрузили, '
                   'поврежден или не является изображением.'
        )

    def follow_unfollow(self, follow, n, a1, a2):
        responses = [
            reverse(f'profile_{follow}',  kwargs={'username': a1.username}),
            reverse(f'profile_{follow}',  kwargs={'username': a2.username}),
        ]
        for r in responses:
            self.client.get(r)
        self.assertEqual(self.user.follower.all().count(), n)

    def create_users(self):
        # создаем пользователей
        a1 = User.objects.create_user(
            username='a1',
        )
        a2 = User.objects.create_user(
            username='a2',
        )
        Post.objects.create(
            text='text',
            group=self.group,
            author=a1
        )
        Post.objects.create(
            text='text',
            group=self.group,
            author=a2
        )

    def follow(self):
        self.create_users()
        author_1 = User.objects.get(username='a1')
        author_2 = User.objects.get(username='a2')
        Follow.objects.create(user=self.user, author=author_1)
        Follow.objects.create(user=self.user, author=author_2)

    def test_auth_user_can_follow(self):
        self.create_users()
        author_1 = User.objects.get(username='a1')
        author_2 = User.objects.get(username='a2')
        self.follow_unfollow('follow', 2, author_1, author_2)
        self.assertEqual(Follow.objects.count(), 2)

    def test_auth_user_can_unfollow(self):
        self.follow()
        author_1 = User.objects.get(username='a1')
        author_2 = User.objects.get(username='a2')
        self.assertEqual(self.user.follower.all().count(), 2)
        self.follow_unfollow('unfollow', 0, author_1, author_2)

    def test_not_auth_user_cant_follow(self):
        response = self.c.get(reverse('profile_follow', kwargs={'username': self.user}))
        login_url = reverse('login')
        profile_url = reverse('profile_follow', kwargs={'username': self.user})
        target_url = f'{login_url}?next={profile_url}'
        self.assertRedirects(response, target_url)
        self.assertEqual(Follow.objects.count(), 0)

    def test_not_auth_user_cant_unfollow(self):
        test_user = User.objects.create_user(username='user')
        Follow.objects.create(user=self.user, author=test_user)
        response = self.c.get(reverse('profile_unfollow', kwargs={'username': test_user}))
        login_url = reverse('login')
        profile_url = reverse('profile_unfollow', kwargs={'username': test_user})
        target_url = f'{login_url}?next={profile_url}'
        self.assertRedirects(response, target_url)
        self.assertEqual(Follow.objects.count(), 1)

    def test_posts_author_follow(self):
        self.follow()
        responses = [
            reverse('follow_index')
        ]
        self._check_posts(responses, 'text', self.group, 2)

    def test_posts_author_not_follow(self):
        responses = [
            reverse('follow_index')
        ]
        self._check_posts(responses, 'text', self.group, 0)

    def test_posts_author_unfollow(self):
        self.create_users()
        response = self.client.get(reverse('follow_index'))
        self.assertEqual(response.status_code, 200)
        paginator = response.context.get('paginator')
        self.assertEqual(paginator.count, 0)

    def test_auth_comment(self):
        post = Post.objects.create(author=self.user, text='text')
        response = self.client.post(
            reverse(
                'add_comment',
                args=[self.user, post.id],
            ),
            {'text': 'comment'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)
        comment = post.comments.first()
        comment_page = response.context['items'][0]
        self.assertEqual(comment_page.text, comment.text)
        self.assertEqual(comment_page.author, comment.author)

    def test_not_auth_comment(self):
        post = Post.objects.create(author=self.user, text='text')
        response = self.c.post(
            reverse(
                'add_comment',
                args=[self.user, post.id],
            ),
            {'text': 'comment'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)

    def test_cache_clear(self):
        post = Post.objects.create(
            text='asdlakwejla,m uwh wpofkwe',
            group=self.group,
            author=self.user
        )
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.text)
        post.delete()
        self.assertContains(response, post.text)
        cache.clear()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, post.text)
