from django.urls import path,re_path,include
from rest_framework.urlpatterns import format_suffix_patterns
from blog import views
from rest_framework.schemas import get_schema_view
from .views import (
    blog_post_detail_view,
    blog_post_list_view,
    blog_post_update_view,
    blog_post_delete_view,
    SnippetList,
    SnippetDetail,
    api_root,
)
"""from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)"""


from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
sitemaps = { 'posts': PostSitemap,}


app_name = 'blog'

schema_view = get_schema_view(title='SCHEMA API')
urlpatterns = [
    path('', blog_post_list_view, name= 'list-view'),
    path('tag/<slug:tag_slug>/',  blog_post_list_view, name='post_list_by_tag'),
    path('<str:slug>', blog_post_detail_view,name='detail-view'),
    path('<str:slug>/edit/', blog_post_update_view,name='update-view'),
    path('<str:slug>/delete/', blog_post_delete_view,name='delete-view'),
    path('api/', api_root, name='api'),
    path('api/schema/', schema_view),
    path('api/snippets/', views.SnippetList.as_view(), name='snippet-list'),
    path('api/snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
    path('api/users/', views.UserList.as_view(), name='user-list'), # new
    path('api/users/<int:pk>/', views.UserDetail.as_view(),name='user-detail'),
    #path('api-token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
