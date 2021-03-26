from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignInForm, ProductForm, SignUpForm, ProductSellForm
from django.db import models
from django.contrib.auth import login, logout, authenticate
from django.views import View
from applications.shop import models
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
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
    allow_empty = True
    ordering = ['-id']


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
        context['product_edit_form'] = ProductForm
        return context


class ProductCreateView(CreateView):
    template_name = 'product_create.html'
    model = models.Product
    fields = '__all__'
    success_url = '/'


class ProductSellView(DetailView):
    model = models.ProductSell
    fields = ['quantity']


class ProductSellListView(ListView):
    model = models.ProductSell
    fields = '__all__'
    paginate_by = 10
    template_name = "sell_list.html"
    allow_empty = True
    ordering = ['-id']

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_superuser:
            queryset = models.ProductSell.objects.all()
        else:
            queryset = models.ProductSell.objects.filter(user_id=user_id)
        return queryset


class ProductIncomeView(CreateView):
    model = models.ProductIncome
    fields = ['product', 'quantity']
    template_name = "product_income.html"

    def post(self, request, *args, **kwargs):
        models.ProductIncome.objects.create(
            user=request.user,
            product_id=request.POST.get('product', None),
            quantity=request.POST.get('quantity', None)
        )
        return redirect('home')

class ProductSellDetailView(DetailView):
    all