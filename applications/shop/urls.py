from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import signin, signup, signout, ProductListView, ProductDetailView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        route='',
        view=login_required(
            ProductListView.as_view(),
            login_url='signin/'
        ),
        name='home'),
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
    )
] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)
