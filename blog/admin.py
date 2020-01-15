from django.contrib import admin

from .models import BlogPost




@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):

    list_display = ('title', 'slug','user', 'publish_date',)
    list_filter = ( 'timestamp', 'publish_date', 'user')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    #raw_id_fields = ('user',)
    date_hierarchy = 'publish_date'
    ordering = ('publish_date','timestamp')