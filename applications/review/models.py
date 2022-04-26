from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from applications.product.models import Element

User = get_user_model()


class Rating(models.Model):
    """
    Модель Рейтинга
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='rating')
    rating = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])

    def __str__(self):
        return f'{self.user} - {self.rating}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Like(models.Model):
    """
    Модель Лайков
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='like')
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.like}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Comment(models.Model):
    """
    Модель Отзывов
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    element = models.ForeignKey(Element,on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField()

    def __str__(self):
        return f'{self.user} - {self.comment}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
