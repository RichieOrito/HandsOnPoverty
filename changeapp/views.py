from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages


def registerPage(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('login')
    
    context={'form':form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    context={}
    return render(request, 'accounts/login.html', context)



def welcome(request):
    return render(request, 'index.html')

# Create your views here.
