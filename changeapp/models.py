from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from tinymce.models import HTMLField
from django.core.validators import MinValueValidator 


User=settings.AUTH_USER_MODEL

# Create your models here.

#User model
class User(AbstractUser):
    full_name = models.CharField(max_length=124)
    email = models.CharField(max_length=124, unique=True)
    avatar = CloudinaryField('image', null=True)
    bio = models.TextField(max_length=500, null=True)
    contact = models.TextField(max_length=20, null=True,)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    @property
    def url_formatted_name(self):
        return self.full_name.replace(' ', '+') or self.username

    @property
    def post_image(self):
        return self.image.build_url(format='webp')

    @property
    def user_avatar(self):
        return self.avatar if self.avatar else f'https://ui-avatars.com/api/?name={self.url_formatted_name}&background=008000&color=000'
    
    def save_user(self):
         self.save()

    @classmethod
    def get_all_users(cls):
        return cls.objects.all()    

#Categories model
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def save_category(self):
        self.save()
    
    @classmethod
    def get_all_categories(cls):
        return cls.objects.all()  

#Articles model
class Articles(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField()
    image  = image = CloudinaryField('image', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # save post
    def save_post(self):
        self.save()

    # delete post
    def delete_post(self):
        self.delete()

    # update post
    def update_post(self):
        self.update()

    @classmethod
    def get_post_by_id(cls, id):
        return cls.objects.get(id = id)

    # search post
    @classmethod
    def search_by_title(cls, search_term):
        post = cls.objects.filter(title__icontains=search_term)
        return post

    # find post by id
    @classmethod
    def find_post(cls, id):
        post = cls.objects.get(id=id)
        return post

    @classmethod
    def get_all_posts(cls):
        return cls.objects.all()

    
    @classmethod
    def search_by_title(cls, title):
        article = Articles.objects.filter(title__icontains = title).first()
        return article 

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_posted']

#Donations from articles Model
class ArticleDonations(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date_donated = models.DateField(auto_now_add=True)

#comments model
class Comments(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    date_commented = models.DateField(auto_now_add=True)
    comment = models.TextField()

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# M-pesa Payment models

class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'


class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'


class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.first_name
