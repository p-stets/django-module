from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager

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

    class Meta:
        abstract = True

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class User(AbstractUser, DateMixin):

    '''
    '''

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    username = models.CharField(max_length=50, verbose_name='Nick-name')
    email = models.EmailField(unique=True)


# class Admin(User):

#     pass


# class Customer(User):

#     '''
#     Platform customer
#     '''

#     credit_limit = models.PositiveIntegerField(verbose_name='Customer credit limit')


class Product(DateMixin):

    '''
    A class for products
    '''

    name = models.CharField(verbose_name='Product name', unique=True, max_length=120)
    price = models.PositiveIntegerField(name='Product price')
    image = models.ImageField(verbose_name='Product Image', upload_to='uploads/')

    @property
    def absolute_path(self):
        return f'{self.image.name}'

    def __str__(self):
        return f'{self.id} - {self.name}'


class ProductIncome(ProductMovementMixin):
    pass


class ProductReturn(ProductMovementMixin):
    pass
