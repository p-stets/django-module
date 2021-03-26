from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignInForm, ProductForm, SignUpForm, ProductSellForm
from django.contrib.auth import login, logout, authenticate
from django.views import View
from applications.shop import models
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def signin(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignInForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # some actions
            login(request, form.user)
            return redirect('home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('email')
            # raw_password = form.cleaned_data.get('password')
            # # user = authenticate(username=username, password=raw_password)
            # # login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request=request,
                  template_name='signup.html',
                  context={'form': form}
                  )


def signout(request):
    logout(request)
    return redirect('home')


# @login_required(login_url='signin/')

class ProductListView(ListView):
    model = models.Product
    paginate_by = 10
    queryset = models.Product.objects.all()
    template_name = "products_list.html"


class ProductDetailView(DetailView):
    http_method_names = ['get', 'post']
    model = models.Product
    template_name = "product_detail.html"

    def post(self, request, *args, **kwargs):
        models.ProductSell.objects.create(
            user=request.user,
            product_id=request.POST.get('product_id', None),
            quantity=request.POST.get('quantity', None)
        )
        return HttpResponseRedirect(request.path_info)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['form'] = ProductSellForm
        return context


class ProductSellView(DetailView):
    model = models.ProductSell
    fields = ['quantity']


def buy_product(request):
    if request.method == 'POST':
        user_id = request.user.id
        product = request.product
