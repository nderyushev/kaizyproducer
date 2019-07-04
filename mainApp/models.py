from django.db import models
from django.urls import reverse
from util import customize_foldername


class Category(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


class Beat(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None)
    category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=None)
    cover = models.ImageField(default=None, upload_to=customize_foldername)
    available = models.BooleanField(default=True)
    bpm = models.IntegerField(default=None)
    track = models.FileField(default=None)
    tonality = models.CharField(max_length=255, default='')


    class Meta:
        verbose_name = 'Beat'
        verbose_name_plural = 'Beats'

    def __str__(self):
        return self.title

    def get_payment_url(self):
        return reverse('payment', kwargs={'beat_slug': self.slug})

class CartItem(models.Model):

    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return "Cart item for beat {}".format(self.beat.title)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'


class Cart(models.Model):

    beats = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def add_to_cart(self, beat_slug):
        cart = self
        beat = Beat.objects.get(slug=beat_slug)
        new_item, _ = CartItem.objects.get_or_create(beat=beat)
        if new_item not in cart.beats.all():
            cart.beats.add(new_item)
            cart.save()

    def remove_from_cart(self, beat_slug):
        cart = self
        beat = Beat.objects.get(slug=beat_slug)
        for item in cart.beats.all():
            if item.beat == beat:
                cart.beats.remove(item)
                cart.save()


