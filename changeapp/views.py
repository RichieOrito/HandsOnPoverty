from unicodedata import category
from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, ArticlesForm, ProfileForm, UpdateArticlesForm, CommentsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Comments, User, Articles, MpesaPayment
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt


def registerPage(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account has been created for ' + user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        else:
            messages.error(request,"Account creation failed")

            
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
            return redirect('index')
        else:
            messages.info(request, 'Email or password is incorrect')
            
    context={}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')

def welcome(request):
    articles = Articles.get_all_posts()
    consumer_key = 'tdGGEWWEx8aSG9wphhreUzIienC91AHP'
    consumer_secret = 'G09hyQp9W6T2Caq4'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return render(request, 'index.html', {'articles':articles} )

#Profile view
def profile(request, username):
    form = ProfileForm
    profile =  User.objects.filter(username = username).first()
    articles = Articles.objects.filter(author = profile).all()

    context = {
         "profile": profile, "form":form, "articles":articles
    }
    return render(request, 'profile.html', context)   
    
@login_required(login_url='login')
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating profile')

        return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def article(request):
    current_user =  request.user
    if request.method == 'POST':
        form = ArticlesForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit =False)
            article.author = current_user
            article.save()
        return redirect('index')

    else:
        form = ArticlesForm()

    return render(request, 'new_article.html', {"form": form})  

def single_article(request, id):
    article = Articles.get_post_by_id(id)
    form = CommentsForm
    comments = Comments.objects.filter(article = article).all()
    return render (request, 'single_article.html', {"article":article, "form":form, "comments":comments})

@login_required(login_url='login')
def delete_article(request, id):
    article = Articles.objects.filter(pk = id).first()
    article.delete()
    return redirect(request.META.get('HTTP_REFERER'), {'success': 'Article deleted successfully'})

@login_required(login_url='login')
def update_article(request, id):
    if request.method == 'POST':
        article = Articles.get_post_by_id(id)
        form = UpdateArticlesForm(request.POST,request.FILES, instance=article)

        if form.is_valid():
            form.save()
            print('Update successful')
            messages.success(request, 'Article updated Successfully')

            return redirect(request.META.get('HTTP_REFERER'), {'success': 'Article updated Successfully'})
        else:
             print('Update unsuccessful')   

    return redirect(request.META.get('HTTP_REFERER'), {'error': 'There was an error updating'})

@login_required(login_url='login')
def add_comment(request, id):
    current_user =  request.user
    article = Articles.get_post_by_id(id)
    if request.method == 'POST':
        form = CommentsForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit =False)
            comment.commentor = current_user
            comment.article = article
            comment.save()
        return redirect(request.META.get('HTTP_REFERER'), {'success': 'Commented succesfully'})

    else:
        form = CommentsForm()

def health_articles(request):
    articles = Articles.objects.filter(category = 1).all()
    return render(request, 'articles/health.html', {"articles":articles})

def education_articles(request):
    articles = Articles.objects.filter(category = 2).all()
    return render(request, 'articles/education.html', {"articles":articles})

def water_articles(request):
    articles = Articles.objects.filter(category = 3).all()
    return render(request, 'articles/sanitation.html', {"articles":articles})

@login_required(login_url='login')
def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        results = Articles.search_by_title(search_term)
        message = f"{search_term}"
        print(results) 
        return render(request, 'articles/search.html',{"message":message,"articles": results})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})

@login_required(login_url='login')
def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    if 'amount' in request.GET and request.GET["amount"]:
        amount = request.GET.get("amount")

    if 'phone_number' in request.GET and request.GET["phone_number"]:
        phone_number = request.GET.get("phone_number")    
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,  
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Ruweydha",
        "TransactionDesc": "Changetime"
    }
    print(amount)
    response = requests.post(api_url, json=request, headers=headers)
    return redirect('index')


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://a07d-41-90-176-143.ngrok.io/api/v1/c2b/confirmation",
               "ValidationURL": "https://a07d-41-90-176-143.ngrok.io/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)

    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)

    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],

    )
    payment.save()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))

    