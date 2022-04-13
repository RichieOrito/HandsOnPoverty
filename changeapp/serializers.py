from rest_framework import serializers
from .models import Articles

class ArticlesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Articles
        fields = ('author','post', 'image', 'date_posted')