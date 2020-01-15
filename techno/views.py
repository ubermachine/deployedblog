from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
# Dont Repeat Yourself = DRY

from blog.models import BlogPost


def home_page(request):
    my_title = "Hello there...."
    qs = BlogPost.objects.all()[:5]
    context = {"title": "", 'blog_list': qs}
    return render(request, "home.html", context)



