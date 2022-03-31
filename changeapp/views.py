from django.shortcuts import render

def welcome(request):
    return render(request, 'index.html')

# Create your views here.
