from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, ArticlesForm, ProfileForm, UpdateArticlesForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Articles


def registerPage(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account has been created for ' + user)
            
            return redirect('login')
    
    context={'form':form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.info(request, 'Email or password is incorrect')
            
    context={}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def welcome(request):
    articles = Articles.get_all_posts()

    return render(request, 'index.html', {'articles':articles} )

#Profile view
def profile(request, username):
    form = ProfileForm
    current_user = request.user
    articles = Articles.objects.filter(author = current_user).all()
    profile =  User.objects.filter(username = username).first()
    context = {
         "profile": profile, "form":form, "articles":articles
    }
    return render(request, 'profile.html', context)   
    
@login_required()
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating profile')

        return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def article(request):
    current_user =  request.user
    if request.method == 'POST':
        form = ArticlesForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit =False)
            article.author = current_user
            article.save()
        return redirect('main')

    else:
        form = ArticlesForm()

    return render(request, 'new_article.html', {"form": form})  

@login_required()
def single_article(request, id):
    article = Articles.get_post_by_id(id)
    return render (request, 'single_article.html', {"article":article})

@login_required()
def delete_article(request, id):
    article = Articles.objects.filter(pk = id).first()
    article.delete()
    return redirect(request.META.get('HTTP_REFERER'), {'success': 'Article deleted successfully'})


@login_required()
def update_article(request, id):
    if request.method == 'POST':
        article = Articles.get_post_by_id(id)
        form = UpdateArticlesForm(request.POST, instance=article)

        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            print('Update successful')
            messages.success(request, 'Article updated Successfully')

            return redirect(request.META.get('HTTP_REFERER'), {'success': 'Article updated Successfully'})
        else:
             print('Update unsuccessful')   

    return redirect(request.META.get('HTTP_REFERER'), {'error': 'There was an error updating'})


    