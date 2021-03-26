from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from main_config.settings import MEDIA_URL
from django.contrib.auth.models import AbstractUser

# Create your models here.


class DateMixin(models.Model):

    '''
    Date mixin. Adding created_date and\
        updated_date to all objects
    '''

    class Meta:
        abstract = True

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class ProductMovementMixin(DateMixin):

    '''
    A MixIn for product movement\
        income and outcome
    '''

    RELEVANT = 1
    PENDING_CANCELLATION = 2
    CANCELLED = 3

    STATUSES = (
        (RELEVANT, 'Relevant'),
        (PENDING_CANCELLATION, 'Pending Cancellation'),
        (CANCELLED, 'Cancelled')
    )

    class Meta:
        abstract = True

    user = models.ForeignKey('User', on_delete=models.PROTECT, verbose_name='Author')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.PositiveIntegerField(choices=STATUSES, default=1)

    def __str__(self):
        return f'{self.id} - {self.product}'


class User(AbstractUser, DateMixin):

    '''
    A User.
    '''

    REQUIRED_FIELDS = ['username', 'base_wallet']
    USERNAME_FIELD = 'email'
    username = models.CharField(max_length=50, verbose_name='Nick-name')
    email = models.EmailField(unique=True)
    base_wallet = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Base wallet amount')

    @property
    def current_money(self):
        status_actual = models.Q(status=1)
        status_pending = models.Q(status=2)
        spent_amount_queryset = ProductSell.objects.filter(status_actual | status_pending, user=self.id)
        bought_total = 0
        for obj in spent_amount_queryset:
            bought_total += obj.quantity * obj.product.price
        return self.base_wallet - bought_total


class Product(DateMixin):

    '''
    A class for products
    '''

    name = models.CharField(verbose_name='Product name', unique=True, max_length=120)
    description = models.TextField(verbose_name='Product description', max_length=2000, null=True, blank=True)
    price = models.DecimalField(verbose_name='Product price', max_digits=10,
                                decimal_places=2, validators=[MinValueValidator(0.01)])
    image = models.ImageField(verbose_name='Product Image', upload_to='products/', blank=True)

    @property
    def current_stock(self):
        # Set statuses actual and pending cancellation
        status_actual = models.Q(status=1)
        status_pending = models.Q(status=2)
        # Get count of actual product quantity
        stock_queryset = ProductIncome.objects.filter(status_actual | status_pending, product__id=self.id)
        product_total_quantity = 0
        for item in stock_queryset:
            product_total_quantity += item.quantity

        # Get count of bought products
        bought_queryset = ProductSell.objects.filter(status_actual | status_pending, product__id=self.id)
        bought_product_count = 0
        for item in bought_queryset:
            bought_product_count += item.quantity

        return product_total_quantity - bought_product_count

    @property
    def image_path(self):
        return f'{MEDIA_URL}{self.image.name}'

    def __str__(self):
        return f'Product - {self.id} - {self.name}'


class ProductIncome(ProductMovementMixin):
    pass


class ProductSell(ProductMovementMixin):
    def clean(self):
        try:
            product = Product.objects.get(id=self.product_id)
            user = User.objects.get(id=self.user_id)
            if product.current_stock - self.quantity <= 0:
                raise ValidationError({'quantity': 'Not enough in stock'})
            if user.current_money - (product.price * self.quantity) < 0:
                raise ValidationError({'user': 'User doesn\'t have enough money'})
        except (Product.DoesNotExist, User.DoesNotExist):
            product = None
            user = None
