from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from django.db.models import Count
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import BlogPostModelForm
from .models import BlogPost

from taggit.models import Tag

from .serializers import SnippetSerializer, UserSerializer
from rest_framework import generics ,permissions 
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view # new
from rest_framework.response import Response # new
from rest_framework.reverse import reverse # new
from rest_framework.permissions import IsAuthenticated


def blog_post_list_view(request, tag_slug=None):

    qs = BlogPost.objects.all().published() 
    
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        qs = qs.filter(tags__in=[tag])
    paginator = Paginator(qs, 5) # 5 posts in each page 
    
    
    page = request.GET.get('page')    
    try:      
        qs = paginator.page(page)  
    except PageNotAnInteger:    
    # If page is not an integer deliver the first page  
        qs = paginator.page(1)   
    except EmptyPage:      
    # If page is out of range deliver last page of results
        qs = paginator.page(paginator.num_pages)
    

    #if request.user.is_authenticated:
    #    my_qs = BlogPost.objects.filter(user=request.user)
    #    qs = (qs | my_qs).distinct()
    template_name = 'blog/list.html'
    context = {'page': page,'object_list': qs,'tag': tag}
    return render(request, template_name, context) 

def blog_post_detail_view(request, slug):
    
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/detail.html'
   
    post_tags_ids = obj.tags.values_list('id', flat=True)
    
    similar_posts = BlogPost.objects.all().published().filter(tags__in=post_tags_ids)\
                                  .exclude(id=obj.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags',)[:4]#'-publish'

    context = {"object": obj, "similar_posts": similar_posts}



    return render(request, template_name, context)   











# @login_required
@staff_member_required
def blog_post_create_view(request):

    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = BlogPostModelForm()
    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)  






@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = 'form.html'
    context = {"title": f"Update {obj.title}", "form": form}
    return render(request, template_name, context)  


@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {"object": obj}
    return render(request, template_name, context)  



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('blog:user-list', request=request, format=format),
        'snippets': reverse('blog:snippet-list', request=request, format=format)
        
    })

class SnippetList(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = SnippetSerializer
    def perform_create(self, serializer): # new
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = SnippetSerializer
#For token auth python manage.py drf_create_token vitor
#will need https://www.technozod.com/blog/api/snippets/38/ 'Authorization: Token c5c7148ecae080a1122a6b1d2372ca0443077d6a'
#permission_classes = (IsAuthenticated,)  
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    
class UserList(generics.ListAPIView): # new
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView): # new
    queryset = User.objects.all()
    serializer_class = UserSerializer

  
