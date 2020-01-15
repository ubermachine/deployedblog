from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

User = settings.AUTH_USER_MODEL

from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField	
from ckeditor_uploader.fields import  RichTextUploadingField
from django.utils.translation import ugettext_lazy as _
class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        tags = TaggableManager()
        return self.filter(publish_date__lte=now)

    def search(self, query):
        lookup = (
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query) |
                    Q(user__username__icontains=query)
                    )

        return self.filter(lookup)


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)


class BlogPost(models.Model): 
    id = models.AutoField(primary_key=True)
    user    = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    image   = models.ImageField(upload_to='image/', blank=True, null=True)
    title  = models.CharField(_('Title'),max_length=120)
    slug   = models.SlugField(unique=True,max_length=200) 
    content  = RichTextUploadingField(null=True, blank=True)
    publish_date = models.DateTimeField(_('Date Published'),auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User',default=1, verbose_name=_(u'Author'),
                                     related_name='snippets',on_delete=models.CASCADE)

    meta_description = models.CharField(
        verbose_name=_('meta description'),
        blank=True, default='',max_length=200)
    meta_keywords = models.CharField(verbose_name=_('meta keywords'),
                                     blank=True, default='',max_length=200)


    objects = BlogPostManager()
    tags = TaggableManager(blank=True,)




    class Meta:
        verbose_name = _("BlogPost")
        verbose_name_plural = _("BlogPosts")
        ordering = ['-publish_date', '-updated', '-timestamp']

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
    def __str__(self): #show title in blog admin instead of object
        return self.title

 

