from django.db import models


class GameCategories(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='название категории', help_text='категории игр<br>представленных на нашем сайте')
    description = models.TextField(blank=True, verbose_name='описание')
    is_active = models.BooleanField(verbose_name='активна', default=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Games(models.Model):

    game_category = models.ForeignKey(GameCategories, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True, verbose_name='название')
    image = models.ImageField(upload_to='game_images', blank=True)
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    quantity = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    class Meta:
        verbose_name = 'игра'
        verbose_name_plural = 'игры'

    def __str__(self):
        return f'{self.name} ({self.game_category.name})'


class DiscountGames(models.Model):
    game_category = models.ForeignKey(GameCategories, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True, verbose_name='название')
    image = models.ImageField(upload_to='game_images')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    old_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    class Meta:
        verbose_name = 'игра со скидкой'
        verbose_name_plural = 'игры со скидкой'

    def __str__(self):
        return f'{self.name} ({self.game_category.name})'


class Contacts(models.Model):
    description = models.TextField(blank=True, verbose_name='описание')
    address = models.TextField(verbose_name='адрес')
    phone = models.CharField(max_length=40, verbose_name='телефон')
    fax = models.CharField(max_length=40, verbose_name='факс')
    email = models.EmailField(verbose_name='почта')
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.address



