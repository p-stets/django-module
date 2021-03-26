from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import signin, signup, signout, ProductListView, ProductDetailView, ProductCreateView, ProductIncomeView, ProductSellListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        route='',
        view=login_required(
            ProductListView.as_view(),
            login_url='signin/'
        ),
        name='home'),
    path(
        route='new_product/',
        view=login_required(
            ProductCreateView.as_view(),
            login_url='signin/'
        ),
        name='new_product'),
    path(
        route='product_income/',
        view=login_required(
            ProductIncomeView.as_view(),
            login_url='signin/'
        ),
        name='product_income'),
    path(
        route='orders/',
        view=login_required(
            ProductSellListView.as_view(),
            login_url='signin/'
        ),
        name='orders'),
    path('signin/', view=signin, name='signin'),
    path('signup/', view=signup, name='signup'),
    path('signout/', view=signout, name='signout'),
    path(
        route='<int:pk>/',
        view=login_required(
            ProductDetailView.as_view(),
            login_url='signin/'
        ),
        name='product_details'
    ),
    path(
        route='orders/<int:pk>/',
        view=login_required(
            ProductDetailView.as_view(),
            login_url='signin/'
        ),
        name='order_details'
    )
] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)
