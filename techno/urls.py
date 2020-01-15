from django.conf import settings
from django.views.generic import TemplateView #remove after anglar test
from django.contrib import admin
from django.urls import path, re_path, include 
from blog.views import (
    blog_post_create_view,
    
)

from searches.views import search_view
from .views import (
    home_page,

)
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
sitemaps = { 'posts': PostSitemap,}


urlpatterns = [
    path('', home_page),
    path('api-auth/', include('rest_framework.urls')),
    path('blog-new/', blog_post_create_view),
    path('blog/', include('blog.urls' , namespace='blog')),
    path('search/', search_view),
    path('1234567899/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),  
    path('angular/', TemplateView.as_view(template_name='ng.html'), name='Angularhome'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
]
#urlpatterns += [
 #   path(r'^(?P<path>.*)', home_page]
if settings.DEBUG:
    # test mode
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






