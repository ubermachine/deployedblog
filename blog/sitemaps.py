from django.contrib.sitemaps import Sitemap 
from .models import BlogPost
class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9
    def items(self):
        return BlogPost.objects.all().published()
    def lastmod(self, obj):
        return obj.updated
