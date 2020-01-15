from rest_framework import serializers
from .models import BlogPost
from django.contrib.auth.models import User

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    url = serializers.HyperlinkedIdentityField(view_name="blog:snippet-detail")
    
    class Meta:
        model = BlogPost
        fields = ('url','id','slug', 'title', 'content','publish_date','owner' )
        
        
        
class UserSerializer(serializers.HyperlinkedModelSerializer): # new
    snippets = serializers.HyperlinkedRelatedField( # new
        many=True, view_name='blog:snippet-detail', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="blog:user-detail")
    class Meta:
        model = User
        fields = ('url','id', 'username', 'snippets')