from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.


def homepage(reuest):
    return HttpResponse('<h1>AAAA</h1>')
