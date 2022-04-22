import shutil

from django import forms
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Follow, Group, Post, User
from ..tests import constants


@override_settings(MEDIA_ROOT=constants.TEMP_MEDIA_ROOT)
class PostsViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username=constants.USERNAME
        )
        cls.user_following = User.objects.create_user(
            username=constants.USERNAME_FOLLOWING
        )
        cls.image = SimpleUploadedFile(
            name=constants.TEST_SMALL_GIF_NAME,
            content=constants.TEST_SMALL_GIF,
            content_type='image/gif'
        )
        cls.group = Group.objects.create(
            title=constants.GROUP_TITLE,
            slug=constants.GROUP_SLUG,
            description=constants.GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=constants.POST_TEXT,
            group=PostsViewTests.group,
            image=cls.image,
        )
        cls.group_1 = Group.objects.create(
            title=f'{constants.GROUP_TITLE}_1',
            slug=f'{constants.GROUP_SLUG}_1',
            description=f'{constants.GROUP_DESCRIPTION}_1',
        )

        cls.INDEX = ('posts/index.html', reverse('posts:index'))
        cls.GROUP_LIST = ('posts/group_list.html', reverse(
            'posts:group_list', kwargs={'slug': cls.group.slug}))
        cls.PROFILE = ('posts/profile.html', reverse(
            'posts:profile', kwargs={'username': cls.user.username}))
        cls.POST_DETAIL = ('posts/post_detail.html', reverse(
            'posts:post_detail', kwargs={'post_id': cls.post.id}))
        cls.POST_CREATE = ('posts/post_create.html', reverse(
            'posts:post_create'))
        cls.POST_EDIT = ('posts/post_create.html', reverse(
            'posts:post_edit', kwargs={'post_id': cls.post.id}))
        cls.ADD_COMMENT = ('posts/post_detail.html', reverse(
            'posts:add_comment', kwargs={'post_id': cls.post.pk}))
        cls.FOLLOW = ('posts/follow.html', reverse('posts:follow_index'))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(constants.TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post_1 = Post.objects.create(
            text=f'{constants.POST_TEXT}_1',
            author=self.user,
            group=self.group_1,
            image=self.image,
        )

    def _test_context_equality(self, test_obj, ref_obj, check_field_list=[]):
        for field in check_field_list:
            self.assertTrue(
                hasattr(test_obj, field) and hasattr(ref_obj, field))
            self.assertEqual(getattr(ref_obj, field), getattr(test_obj, field))

    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_reverse_names = (
            self.INDEX,
            self.GROUP_LIST,
            self.PROFILE,
            self.POST_DETAIL,
            self.POST_CREATE,
            self.POST_EDIT,
            self.ADD_COMMENT,
            self.FOLLOW,
        )
        for template, reverse_name in templates_reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_shows_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.INDEX[1])
        post_object = response.context['page_obj'][1]
        self._test_context_equality(
            post_object, self.post, ['text', 'group', 'author', 'image'])

    def test_group_posts_page_shows_correct_context(self):
        """Шаблон Group сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.GROUP_LIST[1])
        post_object = response.context['group']
        self._test_context_equality(
            post_object, self.group, [
                'title', 'slug', 'description'])
        post_object = response.context['page_obj'][0]
        self.assertEqual(post_object.image, self.post.image)

    def test_profile_page_shows_correct_context(self):
        """Шаблоны Profile сформированы с правильным контекстом."""
        response = self.authorized_client.get(self.PROFILE[1])
        post_object = response.context['page_obj'][1]
        self._test_context_equality(
            post_object, self.post, ['text', 'group', 'author', 'image'])

    def test_post_detail_page_shows_correct_context(self):
        """Шаблон Post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.POST_DETAIL[1])
        self.assertEqual(response.context['post'], self.post)
        self.assertTrue(Post.objects.filter(
            id=self.post.pk,
            image=self.post.image,
        ).exists())

    def test_create_form_shows_correct_context(self):
        """Шаблон Post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.POST_CREATE[1])
        form_fields = {'text': forms.CharField,
                       'group': forms.ModelChoiceField,
                       'image': forms.ImageField,
                       }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        post_object = response.context
        self.assertIn('form', post_object)

    def test_post_edit_form_shows_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.post(self.POST_EDIT[1])
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        post_object = response.context
        self.assertIn('form', post_object)
        self.assertIn('is_edit', post_object)

    def test_add_comment_form_shows_correct_context(self):
        """Шаблон add_comment сформирован с правильным контекстом."""
        response = self.authorized_client.post(self.ADD_COMMENT[1])
        form_field = response.context.get('form').fields.get('text')
        self.assertIsInstance(form_field, forms.fields.CharField)
        post_object = response.context
        self.assertIn('form', post_object)
        self.assertIn('author', post_object)

    def test_new_post_with_group(self):
        self.assertEqual(self.post_1.group, self.group_1)
        self.assertEqual(self.post_1.id, self.group_1.id)
        self.assertEqual(self.post_1.author, self.user)
        self.assertTrue(Post.objects.filter(id=self.post_1.pk).exists())

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


class PostsPaginatedTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=constants.USERNAME)
        cls.group = Group.objects.create(
            title=constants.GROUP_TITLE,
            slug=constants.GROUP_SLUG,
            description=constants.GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=constants.POST_TEXT,
            group=PostsPaginatedTests.group,
        )
        test_post_count = 13
        cls.post = Post.objects.bulk_create([
            Post(author=cls.user,
                 text='Тестовый пост %s' % post_num,
                 group=PostsPaginatedTests.group,
                 )
            for post_num in range(test_post_count)
        ])

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()

    def _get_page_list(self, post_count, limit):
        while post_count > limit:
            page_list = []
            post_count -= limit
            page_list.append(limit)
        else:
            page_list.append(post_count)
        return page_list

    def test_page_paginated(self):
        post_count = Post.objects.count()
        page_list = self._get_page_list(post_count, constants.PAGE_LIMIT)
        for page_number in range(len(page_list)):
            responses = (
                self.authorized_client.get(reverse('posts:index')
                                           + f'?page={page_number + 1}'),
                self.authorized_client.get(reverse(
                    'posts:group_list', kwargs={
                        'slug': self.group.slug
                    }) + f'?page={page_number + 1}'
                ),
                self.authorized_client.get(reverse(
                    'posts:profile', kwargs={
                        'username': self.user.username
                    }) + f'?page={page_number + 1}'
                )
            )
            for response in responses:
                self.assertEqual(
                    len(response.context['page_obj']), page_list[page_number])


class FollowViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username=constants.USERNAME)
        cls.user_following = User.objects.create_user(
            username=constants.USERNAME_FOLLOWING)
        cls.user_follower = User.objects.create_user(
            username=constants.USERNAME_FOLLOWER)
        cls.FOLLOW = ('posts/follow.html', reverse('posts:follow_index'))
        cls.PROFILE_FOLLOW = ('posts/profile.html', reverse(
            'posts:profile_follow',
            kwargs={'username': cls.user_following.username}))
        cls.PROFILE_UNFOLLOW = ('posts/profile.html', reverse(
            'posts:profile_unfollow',
            kwargs={'username': cls.user_following.username}))

    def setUp(self):
        self.authorized_client = Client()
        self.follower_client = Client()
        self.authorized_client.force_login(self.user)
        self.follower_client.force_login(self.user_follower)
        self.follower_client.post(self.PROFILE_FOLLOW[1])
        self.post = Post.objects.create(
            text='Post for followers',
            author=self.user_following,
        )

    def test_follow(self):
        # Подписываемся
        follow_count = Follow.objects.count()
        self.authorized_client.post(self.PROFILE_FOLLOW[1])
        follow = Follow.objects.first()
        self.assertEqual(Follow.objects.count(), follow_count + 1)
        self.assertEqual(follow.author, self.user_following)
        self.assertEqual(follow.user, self.user_follower)

    def test_unfollow(self):
        # Отписываемся
        self.authorized_client.post(self.PROFILE_FOLLOW[1])
        follow_count = Follow.objects.count()
        self.follower_client.get(self.PROFILE_UNFOLLOW[1])
        self.assertEqual(Follow.objects.count(), follow_count - 1)
        self.assertFalse(Follow.objects.filter(
            author=self.user_following,
            user=self.user_follower
        ).exists())

    def test_post_follow_index_for_non_follower(self):
        self.assertFalse(Follow.objects.filter(
            author=self.user_following,
            user=self.user
        ).exists())
        response = self.authorized_client.get(self.FOLLOW[1])
        posts = Post.objects.filter(author=self.user_following)
        follow_index_post = response.context['post_list']
        self.assertNotIn(posts, follow_index_post)

    def test_post_follow_index_for_follower(self):
        self.assertTrue(Follow.objects.filter(
            author=self.user_following,
            user=self.user_follower
        ).exists())
        response = self.follower_client.get(self.FOLLOW[1])
        follow_index_post = response.context['page_obj'][0]
        self.assertEqual(follow_index_post.text, self.post.text)

    def test_no_self_follow(self):
        constraint_name = 'prevent_self_follow'
        with self.assertRaisesMessage(IntegrityError, constraint_name):
            Follow.objects.create(user=self.user, author=self.user)
