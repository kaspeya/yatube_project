from django import forms
from django.core.exceptions import ValidationError
from pytils.translit import slugify

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
        widget = {
            'text': forms.Textarea(attrs={'cols': 40, 'rows': 10})
        }

    # Валидация поля slug
    @property
    def clean_slug(self):
        """Обрабатывает случай, если slug не уникален."""
        cleaned_data = super().clean()
        slug = cleaned_data['slug']
        if not slug:
            title = cleaned_data['slug']
            slug = slugify(title)[:100]
        if Post.objects.filter(slug=slug).exists():
            raise ValidationError(
                f'Адрес "{slug}"'
                f' уже существует, придумайте уникальное значение')
        return slug


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
