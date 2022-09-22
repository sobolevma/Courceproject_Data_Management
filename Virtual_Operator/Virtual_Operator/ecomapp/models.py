from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    # Название категории
    name = models.CharField(max_length=100, )
    # Ссылка на категорию, которую с admin можно не заполнять
    slug = models.SlugField(blank=True, )

    # Возвращаем название категории
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


# Функция заполняющая, поле slug категории, если оно не было заполнено.
def presave_category_slug(sender, instance, *args, **kwargs):
        # if not instance.slug:
        # Преобразем с помощью функции slugify газвание категории в ссылку при помощью функции translit.
        # translit преобразует имя категории в латинские буквы.
        # Ставим reverced=true для передачи русскоязычного названия в translit
        slug = slugify(translit(str(instance.name), reversed=True))

        # Присваиваем новый slug
        instance.slug = slug.replace('-', '_')


# Соединяем сигнал с моделью, т.е. перемещаемя в начало метода save.
pre_save.connect(presave_category_slug, sender=Category)


class Brand(models.Model):
    # Название категории
    name = models.CharField(max_length=100, )

    # Возвращаем название бренда
    def __str__(self):
        return self.name


# Возвращаем файл-картинку по названию и исходному названию файла-картинки
def image_folder(instance, filename):
    # Берем название товара и расширение файла картинки (все что после точки) для создания нового имени файла.
    # Мы составим имя нового файла по названию и расширению
    filename = instance.title + '.' + filename.split('.')[1]
    # Пересохраняем наш фал в папку media в виде: .../media/slug/filename
    return "{0}/{1}".format(instance.slug, filename)


class Service(models.Model):
    # Категория услуги
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    # Название бренда
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    # Название услуги
    title = models.CharField(max_length=120, unique=True)
    # Ссылка на услугу
    slug = models.SlugField(blank=True, )
    # Описание услуги
    description = models.TextField()
    # Картинка к услуге
    image = models.ImageField(upload_to=image_folder)
    # Цена услуги
    price = models.DecimalField(max_digits=9, decimal_places=2)

    # Возвращаем название товара
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'service_slug': self.slug})


def presave_service_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        # Преобразем с помощью функции slugify газвание категории в ссылку при помощью функции translit.
        # translit преобразует имя категории в латинские буквы.
        # Ставим reverced=true для передачи русскоязычного названия в translit
        slug = slugify(translit(str(instance.title), reversed=True))

        # Присваиваем новый slug
        instance.slug = slug.replace('-', '_')


pre_save.connect(presave_service_slug, sender=Service)


# Класс Phone прописываем user.
class Phone(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Номер на который подключается услуга

    phone_number = models.CharField(max_length=15,)

    # slug = models.SlugField(blank=True, )

    # Возвращаем название товара2
    def __str__(self):
        return self.phone_number


# def presave_phone_slug(sender, instance, *args, **kwargs):
        #  if not instance.slug:

        # slug = slugify(instance.phone_number)
# instance.slug = slug.replace('-', '_')


# pre_save.connect(presave_phone_slug, sender=Phone)


class CartItem(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return 'Элемент корзины для услуги {0}'.format(str(self.service.title)
                                                                           )


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, service_slug):
        cart = self
        service = Service.objects.get(slug=service_slug)
        new_item, __ = CartItem.objects.get_or_create(service=service, item_total=service.price)
        # Переделать условие для возможности добавлять несколько номеров
        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, service_slug):
        cart = self
        service = Service.objects.get(slug=service_slug)
        for cart_item in cart.items.all():
            if cart_item.service == service:
                cart.items.remove(cart_item)
                cart.save()


ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен')

)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ForeignKey(Cart, on_delete=models.CASCADE, default='')
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=200,)
    last_name = models.CharField(max_length=200,)
    third_name = models.CharField(max_length=200, )
    order_phone = models.CharField(max_length=15,)
    address = models.CharField(max_length=250, )
    buying_type = models.CharField(max_length=40, choices=(('В офисе', 'В офисе'), ('Доставка', 'Доставка')),
                                   default='В офисе')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

    def __str__(self):
        return 'Заказ №{0}'.format(str(self.id))