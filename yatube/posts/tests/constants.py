import tempfile

POST_TEXT = 'Тестовый пост'
GROUP_TITLE = 'Тестовая группа'
GROUP_SLUG = 'test-slug'
GROUP_DESCRIPTION = 'Тестовое описание'
USERNAME = 'Test User'
USERNAME_FOLLOWING = 'Joanna'
USERNAME_FOLLOWER = 'Wonka'
PAGE_LIMIT = 10
PAGE_NUMBER = 'page'
TEST_GIF = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
    b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
    b"\x02\x4c\x01\x00\x3b"
)
TEST_SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00'
    b'\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
    b'\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)

TEST_SMALL_GIF_NAME = 'small.gif'
TEST_GIF_NAME = 'test.gif'

# Создаем временную папку для медиа-файлов;
# на момент теста медиа папка будет переопределена
TEMP_MEDIA_ROOT = tempfile.gettempdir()


TEST_COMMENT_TEXT = 'Тестовый комментарий'
