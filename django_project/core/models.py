from django.conf import settings
from django.db import models
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('S', 'Компьютеры'),
    ('SW', 'Бытовая Техника'),
    ('OW', 'Телефоны и Аксессуары')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Item(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    price = models.FloatField(verbose_name='Цена')
    discount_price = models.FloatField(
        blank=True, null=True, verbose_name='Цена по скидке')
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=2, verbose_name='Категория')
    label = models.CharField(choices=LABEL_CHOICES,
                             max_length=1, verbose_name='Метка')
    slug = models.SlugField()
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add_to_cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove_from_cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='Пользователь')
    ordered = models.BooleanField(default=False, verbose_name='Заказанный')
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name_plural = 'Заказы Продукта'
        verbose_name = 'Заказ Продукта'

    def __str__(self):
        return f"{self.quantity} {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price - self.get_total_discount_item_price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='Пользователь')
    items = models.ManyToManyField(OrderItem, verbose_name='Товары')
    start_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Начальная Дата')
    ordered_date = models.DateTimeField(verbose_name='Дата Заказа')
    ordered = models.BooleanField(default=False, verbose_name='Заказанный')

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'

    def __str__(self):
        return self.user.username
