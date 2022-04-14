from rest_framework import serializers
from .models import Articles

class ArticlesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Articles
        fields = ('__all__')
        
        