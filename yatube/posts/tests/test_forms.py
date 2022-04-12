import shutil

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Group, Post, User
from ..tests import constants


@override_settings(MEDIA_ROOT=constants.TEMP_MEDIA_ROOT)
class PostsFormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=constants.USERNAME)
        cls.not_author_client = User.objects.create_user(username='NoName')
        cls.group = Group.objects.create(
            title=constants.GROUP_TITLE,
            slug=constants.GROUP_SLUG,
            description=constants.GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=constants.POST_TEXT,
            group=PostsFormsTests.group,
        )
        cls.group_2 = Group.objects.create(
            title=f'{constants.GROUP_TITLE}_2',
            slug=f'{constants.GROUP_SLUG}_2',
            description=f'{constants.GROUP_DESCRIPTION}_2',
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text=constants.TEST_COMMENT_TEXT,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(constants.TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.not_author_client = Client()

    def test_create_post(self):
        uploaded = SimpleUploadedFile(
            name=constants.TEST_SMALL_GIF_NAME,
            content=constants.TEST_SMALL_GIF,
            content_type='image/gif'
        )
        post_count = Post.objects.count()
        form_data = {
            'text': 'test_text',
            'group': self.group.id,
            'image': uploaded,
        }
        response = self.authorized_client.post(reverse(
            'posts:post_create'),
            data=form_data,
            follow=False
        )
        post = Post.objects.first()
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user}))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(post.author, self.user)
        self.assertTrue(Post.objects.filter(image='posts/small.gif').exists())

    def test_edit_post(self):
        post_count = Post.objects.count()
        form_data = {
            'text': 'test_text_1',
            'group': self.group_2.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=False
        )
        post = Post.objects.get(pk=self.post.pk)
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.pk}))
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, self.group_2.id)

    def test_not_author_trys_edit_post(self):
        form_data = {
            'text': 'test_text_2',
            'group': self.group.id
        }
        self.authorized_client.logout()
        response = self.not_author_client.post(reverse(
            'posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        redirect_url = '{}?next={}'.format(
            reverse('users:login'),
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk})
        )
        self.assertRedirects(response, redirect_url)

    def test_add_comment(self):
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Комментарий для теста'
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=False
        )
        comment = Comment.objects.first()
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.pk}))
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertEqual(comment.text, form_data['text'])

    def test_not_author_trys_comment_post(self):
        form_data = {
            'text': 'Комментарий для теста 2',
        }
        self.authorized_client.logout()
        response = self.not_author_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=False
        )
        redirect_url = '{}?next={}'.format(
            reverse('users:login'),
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk})
        )
        self.assertRedirects(response, redirect_url)

    def test_index_cache(self):
        # Создаем пост, затем удаляем после записи в контент
        cache.clear()
        post_for_cache = Post.objects.create(
            text='КэшТест',
            group=self.group,
            author=self.user
        )
        first_response = self.authorized_client.get(reverse('posts:index'))
        first_object = first_response.content
        post_for_cache.delete()
        # Проверяем кэш
        second_response = self.authorized_client.get(reverse('posts:index'))
        second_object = second_response.content
        self.assertEqual(first_object, second_object)
        cache.clear()
        # Проверяем, что кэш удалился
        last_response = self.authorized_client.get(reverse('posts:index'))
        last_object = last_response.content
        self.assertNotEqual(second_object, last_object)
