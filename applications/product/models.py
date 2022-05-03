from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """
    Моделька категории
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category', blank=True, null=True)

    def __str__(self):
        if not self.parent:
            return f'{self.id}'
        else:
            return f'{self.parent} --> {self.slug}'

    def save(self, *args, **kwargs):
        self.slug = self.title.lower()
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Element(models.Model):
    """
    Моделька отелей
    """
    user = models.ForeignKey(User, related_name='elements', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='elements', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'


class ElementImage(models.Model):
    """
    Моделька Фото
    """
    image = models.ImageField(upload_to='imagesfromsite')
    element = models.ForeignKey(Element, related_name='image', on_delete=models.CASCADE)


class FavouriteElement(models.Model):
    """
    Моделька избранных отелей
    """
    user = models.ForeignKey(User, related_name='favourite', on_delete=models.CASCADE)
    element = models.ForeignKey(Element, related_name='favourite', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Reservation(models.Model):
    """
    Моделька бронировании отели
    """
    user = models.ForeignKey(User, related_name='reservation', on_delete=models.CASCADE)
    element = models.ForeignKey(Element, related_name='reservation', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    confirm_reservation = models.CharField(max_length=8, blank=True)

    def __str__(self):
        return f'{self.element.title}'

    # def create_activation_code(self):
    #     from django.utils.crypto import get_random_string
    #     code = get_random_string(8)
    #     self.confirm_reservation = code
    #     self.save()
    #     return code


class HotelsIk(models.Model):
    """
    Модельки данных с парсинга
    """
    title = models.CharField(max_length=100)
    rating = models.CharField(max_length=20)
    ratingcount = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images', blank=True, null=True)


