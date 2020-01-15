from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import BlogPost 

class BlogPostForm(forms.Form):
    title = forms.CharField()
    #slug = forms.SlugField()
    #content = forms.CharField(widget=forms.Textarea)
    content = forms.CharField(widget=CKEditorWidget())


class BlogPostModelForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = BlogPost
	
        fields = ['title', 'image', 'content', 'publish_date']

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = BlogPost.objects.filter(title__iexact=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk) # id=instance.id
        if qs.exists():
            raise forms.ValidationError("This title has already been used. Please try again.")
        return title
